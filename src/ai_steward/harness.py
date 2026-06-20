"""Harness-protocol integration for ai-steward.

All LLM calls MUST route through the harness proxy. If the proxy is
unreachable, PRE-FLIGHT fails and no LLM call is made. This is the
structural Observable Autonomy guarantee — not optional.

The proxy speaks standard provider APIs at its local endpoint:
  POST http://localhost:8474/v1/messages          → Anthropic
  POST http://localhost:8474/v1/chat/completions  → OpenAI / Grok

Credentials pass through unchanged (proxy forwards all headers verbatim).
Set base_url in the provider SDK to the value returned by anthropic_base_url().
"""

import os
import socket
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

from ai_steward.config import HarnessConfig


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

    The harness proxy compresses responses with gzip but omits the
    Content-Encoding header, so the SDK's httpx transport cannot
    auto-decompress them. Setting Accept-Encoding: identity in the
    request prevents compression and allows the SDK to parse responses
    correctly.

    When harness_root is provided, the X-Harness-Root header directs the
    proxy to write the session ledger to <harness_root>/sessions/<sid>.jsonl
    instead of the proxy's default root. This is the mechanism that makes
    Observable Autonomy structural: sessions land in the target repo's
    .trail/ directory, co-located with audit-trail.md.

    Usage:
        client = anthropic_client(config.harness, harness_root=repo / ".trail")
        message = client.messages.create(...)
    """
    import anthropic as _anthropic
    import httpx as _httpx

    default_headers: dict[str, str] = {"Accept-Encoding": "identity"}
    if harness_root is not None:
        default_headers["X-Harness-Root"] = str(harness_root)

    return _anthropic.Anthropic(
        base_url=config.endpoint,
        http_client=_httpx.Client(headers=default_headers),
    )


@contextmanager
def harness_session(target_repo: Path, config: HarnessConfig):
    """Context manager that sets HARNESS_ROOT for one pipeline run.

    The harness proxy uses HARNESS_ROOT to determine where to write its
    ledger. Setting it to <target_repo>/.trail co-locates the harness
    evidence (JSONL) with the audit trail memory (audit-trail.md) in the
    .trail/ directory standard — both layers of the two-tier trust model
    are in the same directory tree.

    Yields a dict {"session_path": str | None}. After the context exits,
    session_path is the repo-relative path to the harness session created
    during this run, or None if no session was created (harness not
    running, or no LLM calls were made).

    The previous HARNESS_ROOT value is restored on exit.
    """
    key = "HARNESS_ROOT"
    harness_root = target_repo / ".trail"
    sessions_dir = harness_root / "sessions"

    # Snapshot existing sessions before any calls — used to identify
    # which session was created during this run.
    # Sessions are .jsonl files per SPEC §8.1: <root>/sessions/<sid>.jsonl
    before = (
        {p.name for p in sessions_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
        if sessions_dir.is_dir()
        else set()
    )

    result: dict[str, str | None] = {"session_path": None}
    prev = os.environ.get(key)
    os.environ[key] = str(harness_root)
    try:
        yield result
    finally:
        if prev is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prev
        # Identify the session created during this run by diffing before/after.
        # Sessions are .jsonl files per SPEC §8.1. ULID names are time-ordered;
        # the newest new entry is the one we want.
        if sessions_dir.is_dir():
            after = {p.name for p in sessions_dir.iterdir() if p.is_file() and p.suffix == ".jsonl"}
            new = sorted(after - before)
            if new:
                result["session_path"] = f".trail/sessions/{new[-1]}"
