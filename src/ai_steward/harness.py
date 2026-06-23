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
    proxy via X-Harness-Session.  The proxy groups all calls sharing the same
    X-Harness-Session value into a single session file — one iteration = one
    .jsonl file, with SCAN (seq=0), IMPLEMENT (seq=1), REFLECT (seq=2) chained.
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

    X-Harness-Root is always sent. harness_session() sets HARNESS_ROOT in
    the environment; this function reads it as the default when harness_root
    is not supplied explicitly. A call site can never accidentally omit the
    header — the context manager's guarantee is structural, not a convention.

    harness_root (optional): override the root for this specific call. Rarely
    needed; the env var set by harness_session() is correct in all normal cases.

    Usage (always inside harness_session()):
        with harness_session(repo, config.harness):
            client = anthropic_client(config.harness)   # X-Harness-Root from env
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

    # X-Harness-Root: explicit parameter wins; env var (set by harness_session)
    # is the automatic fallback. Since harness_session() always sets HARNESS_ROOT
    # before yielding, the header is guaranteed on every call with no action
    # required from the caller.
    effective_root: str | None = (
        str(harness_root) if harness_root is not None else os.environ.get("HARNESS_ROOT")
    )

    default_headers: dict[str, str] = {"Accept-Encoding": "identity"}
    if effective_root is not None:
        default_headers["X-Harness-Root"] = effective_root
    if run_id:
        # X-Harness-Session groups all calls sharing this run_id into one
        # session file (SPEC §4.2 sid). Proxy implements this — verified live:
        # one harness_session() produces one .jsonl with 3 hash-chained entries.
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
      call.  The proxy groups all calls sharing this value into one session file.
      One harness_session() == one .jsonl == one pipeline iteration (verified live:
      SCAN seq=0, IMPLEMENT seq=1, REFLECT seq=2 in a single hash-chained file).

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
