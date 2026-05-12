"""
utils/llm.py
------------
Central LLM factory for the multi-agent system.

Why this file exists
--------------------
Every agent (movie, story, router, …) needs a Large Language Model.
Instead of each agent creating its own model — and duplicating
configuration — they all import `get_llm()` from here.

That gives us three big wins:
1.  **One source of truth.**  Change the model, host, or timeout in
    one place and the whole project updates.
2.  **Easy provider swap.**  To move from Ollama to OpenAI or Groq,
    you only touch this file.
3.  **Better debugging.**  Centralised logging + a health check tell
    you immediately when something is wrong with the Ollama server.

Public API
----------
    get_llm(temperature: float = 0.7, max_tokens: int = 1024) -> ChatOllama
    check_ollama_server() -> bool
    OllamaConnectionError                     (raised on connection issues)
"""

from __future__ import annotations

import logging
import os
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Load variables from .env once at import time so every caller benefits.
load_dotenv()

# Defaults can be overridden via environment variables (.env).
DEFAULT_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3:8b")
DEFAULT_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
HEALTH_CHECK_TIMEOUT: float = float(os.getenv("OLLAMA_HEALTH_TIMEOUT", "3.0"))


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
if not logger.handlers:
    # Configure a sensible default so users see logs even without
    # bespoke logging config. Apps can override this freely.
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class OllamaConnectionError(RuntimeError):
    """Raised when the Ollama server cannot be reached or the model is missing."""


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def check_ollama_server(base_url: str = DEFAULT_BASE_URL) -> bool:
    """
    Verify that the Ollama server is reachable.

    Sends a tiny HTTP GET to the server root. Returns True on success
    and False on any network error. Uses only the standard library so
    that callers don't pay an extra dependency for a health check.

    Parameters
    ----------
    base_url : str
        Ollama server base URL (e.g. ``http://localhost:11434``).

    Returns
    -------
    bool
        True if the server responded, False otherwise.
    """
    url = urljoin(base_url, "/")
    try:
        with urlopen(Request(url), timeout=HEALTH_CHECK_TIMEOUT) as resp:
            ok = 200 <= resp.status < 500
            logger.debug("Ollama health check at %s → status %s", url, resp.status)
            return ok
    except URLError as exc:
        logger.debug("Ollama health check failed: %s", exc)
        return False
    except Exception as exc:  # pragma: no cover — defensive catch-all
        logger.debug("Unexpected error during health check: %s", exc)
        return False


# ---------------------------------------------------------------------------
# LLM factory
# ---------------------------------------------------------------------------


def get_llm(
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    model: str | None = None,
    base_url: str | None = None,
) -> ChatOllama:
    """
    Build and return a ChatOllama instance configured for this project.

    Parameters
    ----------
    temperature : float
        Sampling temperature. Lower (~0.0) = deterministic, higher
        (~1.0) = creative. Default 0.7.
    max_tokens : int
        Maximum number of tokens the model is allowed to generate per
        response. Maps to Ollama's ``num_predict`` option.
    model : str, optional
        Model name override. Falls back to ``OLLAMA_MODEL`` env var or
        ``qwen3:8b``.
    base_url : str, optional
        Override for the Ollama server URL.

    Returns
    -------
    ChatOllama
        A ready-to-use LangChain chat model.

    Raises
    ------
    OllamaConnectionError
        If the Ollama server is not reachable or the model fails to
        initialise.
    """
    model_name = model or DEFAULT_MODEL
    server_url = base_url or DEFAULT_BASE_URL

    # ---- 1. Health check -------------------------------------------------
    if not check_ollama_server(server_url):
        msg = (
            f"❌ Cannot reach Ollama at {server_url}. "
            "Is the server running? Start it with `ollama serve` and ensure "
            f"the model is pulled with `ollama pull {model_name}`."
        )
        logger.error(msg)
        raise OllamaConnectionError(msg)

    # ---- 2. Build the model ---------------------------------------------
    try:
        logger.info(
            "Initialising ChatOllama (model=%s, temperature=%s, max_tokens=%s)",
            model_name,
            temperature,
            max_tokens,
        )
        llm = ChatOllama(
            model=model_name,
            base_url=server_url,
            temperature=temperature,
            # Ollama uses `num_predict` to cap generated tokens; the
            # LangChain wrapper passes it through transparently.
            num_predict=max_tokens,
        )
        return llm
    except Exception as exc:
        msg = (
            f"❌ Failed to initialise ChatOllama with model '{model_name}'. "
            f"Original error: {exc}"
        )
        logger.exception(msg)
        raise OllamaConnectionError(msg) from exc


# ---------------------------------------------------------------------------
# Convenience singleton
# ---------------------------------------------------------------------------
#
# Importing `llm` directly is handy for quick prototypes, but it builds
# the model at import time — which means a missing Ollama server will
# crash the importer. We expose it lazily through a function so agents
# can choose: call `get_llm()` for explicit control, or use the
# module-level `llm` for the default config.
#
# Agents in this project should generally prefer `get_llm(...)` so they
# can pick their own temperature.

llm: ChatOllama | None = None


def _ensure_default_llm() -> ChatOllama:
    """Lazily build and cache the default LLM instance."""
    global llm
    if llm is None:
        llm = get_llm()
    return llm


__all__ = [
    "get_llm",
    "check_ollama_server",
    "OllamaConnectionError",
    "_ensure_default_llm",
]
