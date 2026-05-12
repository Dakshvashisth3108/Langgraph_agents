"""
agents/_base.py
---------------
Shared execution pipeline for specialist agents.

Every specialist in this project (MovieAgent, StoryAgent, …) does the
same dance:

    1. Validate the user input.
    2. Load a prompt template from disk.
    3. Fill in ``{history}`` and ``{user_input}``.
    4. Call the shared Ollama LLM.
    5. Return the model's reply as a plain string.

Rather than copy-pasting that flow into every agent, this module
captures it once in ``run_agent()``. New specialists become a handful
of lines: pick a prompt file, pick a temperature, done.

Keeping the helper in ``agents/`` (vs ``utils/``) is intentional — it
belongs alongside the agents that use it, and the leading underscore
signals "internal: not a user-facing module".
"""

from __future__ import annotations

import logging
from pathlib import Path

from langchain_core.messages import BaseMessage

from utils.llm import OllamaConnectionError, get_llm
from utils.memory import format_history_for_prompt


logger = logging.getLogger(__name__)


# Resolve the prompts directory once at import time.
PROMPTS_DIR: Path = Path(__file__).resolve().parent.parent / "prompts"


# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------


def load_prompt(filename: str) -> str:
    """
    Read a prompt template from ``prompts/``.

    Parameters
    ----------
    filename : str
        Base name of the file (e.g. ``"movie_prompt.txt"``).

    Returns
    -------
    str
        The raw template text. Contains ``{user_input}`` and/or
        ``{history}`` placeholders that the caller should fill in.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist — surfaced with a clear path so the
        user knows exactly which file to restore.
    """
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt template not found at {path}. "
            "Make sure the file exists under prompts/."
        )
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Shared agent runner
# ---------------------------------------------------------------------------


def run_agent(
    *,
    agent_name: str,
    prompt_file: str,
    user_input: str,
    history: list[BaseMessage] | None = None,
    temperature: float = 0.7,
    max_tokens: int = 600,
    empty_input_msg: str = "Please share something so I can help!",
) -> str:
    """
    Execute one full specialist turn and return the model's reply.

    Designed to never raise — every error path returns a friendly
    string instead, so the LangGraph workflow and Streamlit UI stay
    responsive even if something goes wrong.

    Parameters
    ----------
    agent_name : str
        Used only for logging (e.g. ``"movie_agent"``).
    prompt_file : str
        Name of the template file under ``prompts/``.
    user_input : str
        The user's message.
    history : list[BaseMessage] | None
        Short-term conversation memory. ``None`` or empty on first turn.
    temperature : float
        Sampling temperature for the LLM call.
    max_tokens : int
        Maximum number of tokens to generate.
    empty_input_msg : str
        Friendly message returned when ``user_input`` is blank.

    Returns
    -------
    str
        The LLM's reply, trimmed; or a friendly error/empty-input
        message if something failed.
    """
    # 1. Fast-fail on blank input — saves an unnecessary model call.
    if not user_input or not user_input.strip():
        logger.warning("%s called with empty input", agent_name)
        return empty_input_msg

    logger.info("%s ▶ %s", agent_name, _truncate(user_input))

    # 2. Load the prompt template (or surface a clear error).
    try:
        template = load_prompt(prompt_file)
    except FileNotFoundError as exc:
        logger.error("%s prompt missing: %s", agent_name, exc)
        return f"⚠️ Internal error: {exc}"

    # 3. Render placeholders.
    history_text = format_history_for_prompt(history or [])
    prompt = template.format(user_input=user_input, history=history_text)

    # 4. Call the LLM, catching the two common failure modes plus a
    #    last-resort catch-all.
    try:
        llm = get_llm(temperature=temperature, max_tokens=max_tokens)
        result = llm.invoke(prompt)
    except OllamaConnectionError as exc:
        logger.error("%s — Ollama unreachable: %s", agent_name, exc)
        return (
            "⚠️ I couldn't reach the local LLM. Please make sure "
            "`ollama serve` is running and `qwen3:8b` is pulled, "
            "then try again."
        )
    except Exception as exc:
        logger.exception("%s failed: %s", agent_name, exc)
        return f"⚠️ Something went wrong while running {agent_name}."

    text = (result.content or "").strip()
    logger.info("%s ◀ %d chars", agent_name, len(text))
    return text


# ---------------------------------------------------------------------------
# Tiny utilities
# ---------------------------------------------------------------------------


def _truncate(text: str, limit: int = 80) -> str:
    """Shorten a string for log readability."""
    text = text.replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


__all__ = ["load_prompt", "run_agent", "PROMPTS_DIR"]
