"""agent-evidence-proxy integration for ai-steward.

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
from ai_steward.memory import resolve_scope

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ULID generation (a ULID satisfies the proxy's session-id validation)
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


def anthropic_client(config: HarnessConfig) -> "anthropic.Anthropic":
    """Anthropic SDK client pre-configured for the harness proxy.

    INVARIANT: This function MUST only be called inside a harness_session()
    context. Calling it outside raises RuntimeError immediately.

    The harness_session() context sets HARNESS_SESSION_ID, which is sent as
    X-Harness-Session so that all calls of one run share one ledger file. The
    capture location is the proxy's own configuration (HARNESS_ROOT at proxy
    start); the client does not choose it.

    Usage (always inside harness_session()):
        with harness_session(repo, config.harness):
            client = anthropic_client(config.harness)
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
    if run_id:
        # Groups all calls sharing this run_id into one ledger file. The proxy
        # accepts only [A-Za-z0-9_-]{1,64}; a ULID qualifies.
        default_headers["X-Harness-Session"] = run_id

    return _anthropic.Anthropic(
        base_url=config.endpoint,
        http_client=_httpx.Client(headers=default_headers),
    )


@contextmanager
def harness_session(target_repo: Path, config: HarnessConfig):
    """Context manager that sets HARNESS_SESSION_ID for one pipeline run.

    HARNESS_SESSION_ID is a per-run ULID forwarded as X-Harness-Session on every API
    call.  The proxy groups all calls sharing this value into one ledger file
    ``<evidence>/<sid>.jsonl``, where ``<evidence>`` is the ``evidence/`` folder of the
    repository's memory scope. The proxy must have been started with HARNESS_ROOT set
    to that folder; the client does not tell it where to write.

    Yields a dict with:
      "session_paths": list[str]  — paths of every .jsonl created in the evidence folder
                                    during the context: ``.acm/evidence/<name>`` for a
                                    legacy repo, absolute paths when bound.
      "run_id":        str         — the ULID generated for this run.

    The variable is restored to its prior value on exit (including on exception).
    """
    sid_key = "HARNESS_SESSION_ID"
    scope = resolve_scope(target_repo)
    evidence_dir = scope.dir / "evidence"
    bound = scope.bound

    run_id = _generate_ulid()

    # Snapshot existing ledger files so the ones created during this run can be reported.
    before = (
        {p.name for p in evidence_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
        if evidence_dir.is_dir()
        else set()
    )

    result: dict[str, list[str] | str] = {"session_paths": [], "run_id": run_id}
    prev_sid = os.environ.get(sid_key)
    os.environ[sid_key] = run_id
    try:
        yield result
    finally:
        if prev_sid is None:
            os.environ.pop(sid_key, None)
        else:
            os.environ[sid_key] = prev_sid
        # ULID names are lexicographically time-ordered — sorted() gives chronological order.
        if evidence_dir.is_dir():
            after = {p.name for p in evidence_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
            names = sorted(after - before)
            result["session_paths"] = (
                [str(evidence_dir / n) for n in names] if bound else [f".acm/evidence/{n}" for n in names]
            )
