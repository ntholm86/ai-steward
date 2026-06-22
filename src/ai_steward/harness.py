"""llm-harness-proxy integration for ai-steward.

All LLM calls MUST route through the harness proxy. If the proxy is
unreachable, PRE-FLIGHT fails and no LLM call is made. This is the
structural Observable Autonomy guarantee — not optional.

The proxy speaks standard provider APIs at its local endpoint:
  POST http://localhost:8474/v1/messages          → Anthropic
  POST http://localhost:8474/v1/chat/completions  → OpenAI / Grok

Credentials pass through unchanged (proxy forwards all headers verbatim).
Set base_url in the provider SDK to the value returned by anthropic_base_url().
"""

from __future__ import annotations

import logging
import os
import socket
import time
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from ai_steward.config import HarnessConfig

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ULID generation (SPEC §4.2: sid MUST be a 26-char Crockford base-32 ULID)
# ---------------------------------------------------------------------------

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _generate_ulid() -> str:
    """Generate a valid 26-character Crockford base-32 ULID.

    Used to produce a pipeline-run identifier that is passed to the harness
    proxy via X-Harness-Session.  When the proxy implements that header, all
    API calls in the same run will share a single session file.  Until then
    the proxy ignores the header and creates one file per call — no regression.
    """
    ts = int(time.time() * 1000)  # milliseconds since epoch
    ts_chars = ""
    t = ts
    for _ in range(10):
        ts_chars = _CROCKFORD[t & 0x1F] + ts_chars
        t >>= 5
    rand_int = int.from_bytes(os.urandom(10), "big")  # 80 bits of randomness
    rand_chars = ""
    for _ in range(16):
        rand_chars = _CROCKFORD[rand_int & 0x1F] + rand_chars
        rand_int >>= 5
    return ts_chars + rand_chars


def is_reachable(config: HarnessConfig) -> bool:
    """TCP-level check that the harness proxy is listening.

    Used in PRE-FLIGHT. Does not send an HTTP request — a TCP connection
    attempt is sufficient to confirm the port is accepting connections.
    Returns True if reachable, False on any connection failure.
    """
    parsed = urlparse(config.endpoint)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 8474
    try:
        with socket.create_connection((host, port), timeout=2.0):
            return True
    except OSError:
        return False


def anthropic_base_url(config: HarnessConfig) -> str:
    """Base URL for the Anthropic SDK pointing at the harness proxy.

    Pass this as base_url when constructing anthropic.Anthropic():

        client = anthropic.Anthropic(
            base_url=anthropic_base_url(config),
            api_key=os.environ["ANTHROPIC_API_KEY"],
        )

    The proxy route is POST /v1/messages — identical to Anthropic's real API.
    """
    return config.endpoint


def anthropic_client(
    config: HarnessConfig,
    harness_root: "Path | None" = None,
) -> "anthropic.Anthropic":
    """Anthropic SDK client pre-configured for the harness proxy.

    INVARIANT: This function MUST only be called inside a harness_session()
    context. Calling it outside raises RuntimeError immediately.

    This is not a convention — it is a hard structural boundary. Every LLM
    API call made by ai-steward must be harness-captured, without exception.
    The harness_session() context sets HARNESS_SESSION_ID, which serves as
    both the session-grouping token and the proof that the caller is operating
    inside the Observable Autonomy boundary.

    When harness_root is provided, the X-Harness-Root header directs the
    proxy to write the session ledger to <harness_root>/sessions/<sid>.jsonl
    instead of the proxy's default root. This is the mechanism that makes
    Observable Autonomy structural: sessions land in the target repo's
    .acm/ directory, co-located with audit-trail.md.

    Usage (always inside harness_session()):
        with harness_session(repo, config.harness):
            client = anthropic_client(config.harness, harness_root=repo / ".acm")
            message = client.messages.create(...)
    """
    import anthropic as _anthropic
    import httpx as _httpx

    run_id = os.environ.get("HARNESS_SESSION_ID")
    if run_id is None:
        raise RuntimeError(
            "anthropic_client() called outside a harness_session() context. "
            "All LLM API calls must be harness-captured — no exceptions. "
            "Wrap this call inside 'with harness_session(repo, config.harness):'."
        )

    default_headers: dict[str, str] = {"Accept-Encoding": "identity"}
    if harness_root is not None:
        default_headers["X-Harness-Root"] = str(harness_root)
    if run_id:
        # X-Harness-Session groups all calls in this pipeline run into one
        # session file once the proxy implements the header (SPEC §4.2 sid).
        # Until then the proxy ignores it — zero behaviour change.
        default_headers["X-Harness-Session"] = run_id

    return _anthropic.Anthropic(
        base_url=config.endpoint,
        http_client=_httpx.Client(headers=default_headers),
    )


@contextmanager
def harness_session(target_repo: Path, config: HarnessConfig):
    """Context manager that sets HARNESS_ROOT and HARNESS_SESSION_ID for one pipeline run.

    Sets two environment variables for the duration of the context:
    - HARNESS_ROOT: directs the proxy to write session ledgers to <target_repo>/.acm/
    - HARNESS_SESSION_ID: a per-run ULID forwarded as X-Harness-Session on every API
      call.  Once the proxy implements that header, all calls in the run will share
      a single session file.  Until then the proxy creates one file per call and
      ignores the header — this change has no observable effect on current proxy
      behaviour, but closes the client side of the protocol gap.

    Yields a dict with:
      "session_paths": list[str]  — repo-relative paths of every .jsonl created
                                    during the context (SCAN + IMPLEMENT + REFLECT).
      "run_id":        str         — the ULID generated for this run.

    Both variables are restored to their prior values on exit (including on exception).
    """
    root_key = "HARNESS_ROOT"
    sid_key = "HARNESS_SESSION_ID"
    harness_root = target_repo / ".acm"
    sessions_dir = harness_root / "sessions"

    run_id = _generate_ulid()

    # Snapshot existing sessions before any calls — used to identify
    # which sessions were created during this run.
    # Sessions are .jsonl files per SPEC §8.1: <root>/sessions/<sid>.jsonl
    before = (
        {p.name for p in sessions_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
        if sessions_dir.is_dir()
        else set()
    )

    result: dict[str, list[str] | str] = {"session_paths": [], "run_id": run_id}
    prev_root = os.environ.get(root_key)
    prev_sid = os.environ.get(sid_key)
    os.environ[root_key] = str(harness_root)
    os.environ[sid_key] = run_id
    try:
        yield result
    finally:
        if prev_root is None:
            os.environ.pop(root_key, None)
        else:
            os.environ[root_key] = prev_root
        if prev_sid is None:
            os.environ.pop(sid_key, None)
        else:
            os.environ[sid_key] = prev_sid
        # Collect ALL new session files created during this run (SCAN + IMPLEMENT +
        # REFLECT).  ULID names are lexicographically time-ordered — sorted() gives
        # chronological order.
        if sessions_dir.is_dir():
            after = {p.name for p in sessions_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
            result["session_paths"] = [f".acm/sessions/{n}" for n in sorted(after - before)]
