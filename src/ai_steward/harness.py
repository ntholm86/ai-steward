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


def anthropic_client(config: HarnessConfig) -> "anthropic.Anthropic":
    """Anthropic SDK client pre-configured for the harness proxy.

    The harness proxy compresses responses with gzip but omits the
    Content-Encoding header, so the SDK's httpx transport cannot
    auto-decompress them. Setting Accept-Encoding: identity in the
    request prevents compression and allows the SDK to parse responses
    correctly.

    Usage:
        client = anthropic_client(config.harness)
        message = client.messages.create(...)
    """
    import anthropic as _anthropic
    import httpx as _httpx

    return _anthropic.Anthropic(
        base_url=config.endpoint,
        http_client=_httpx.Client(headers={"Accept-Encoding": "identity"}),
    )


@contextmanager
def harness_session(target_repo: Path, config: HarnessConfig):
    """Context manager that sets HARNESS_ROOT for one pipeline run.

    The harness proxy uses HARNESS_ROOT to determine where to write its
    ledger. Setting it to <target_repo>/.harness co-locates evidence with
    the target being worked on. The previous value is restored on exit.

    Usage:
        with harness_session(target_repo, config):
            # All LLM calls made here write their ledger to target_repo/.harness
            result = run_pipeline(...)
    """
    key = "HARNESS_ROOT"
    prev = os.environ.get(key)
    os.environ[key] = str(target_repo / ".harness")
    try:
        yield
    finally:
        if prev is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prev
