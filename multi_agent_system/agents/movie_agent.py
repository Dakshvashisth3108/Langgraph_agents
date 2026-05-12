"""
agents/movie_agent.py
---------------------
MovieAgent — a friendly movie expert that explains film stories.

Public API
----------
* ``get_movie_response(user_input, history=None) -> str``
    Standalone helper for scripts, tests, REPLs.
* ``movie_agent(state) -> dict``
    LangGraph node wrapper used by ``graph/workflow.py``.

The actual prompt-loading / LLM-calling / error-handling pipeline
lives in :mod:`agents._base`. This file just configures a movie-flavoured
call to that pipeline, keeping the agent's intent obvious at a glance.
"""

from __future__ import annotations

from langchain_core.messages import BaseMessage

from agents._base import run_agent


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AGENT_NAME: str = "movie_agent"
PROMPT_FILE: str = "movie_prompt.txt"

# Low temperature → factual, deterministic movie summaries.
# Token budget sized for ~120-word replies + the structured header.
MOVIE_TEMPERATURE: float = 0.5
MOVIE_MAX_TOKENS: int = 400

EMPTY_INPUT_MSG: str = "Please tell me which movie you'd like to know about."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_movie_response(
    user_input: str,
    history: list[BaseMessage] | None = None,
) -> str:
    """
    Ask the movie expert about a film and return its reply.

    Parameters
    ----------
    user_input : str
        Whatever the user typed (e.g. "Tell me about Interstellar").
    history : list[BaseMessage] | None
        Past conversation messages, used for follow-up context like
        "what else has that director made?".

    Returns
    -------
    str
        A short, spoiler-light movie summary; or a friendly error
        message if something failed.
    """
    return run_agent(
        agent_name=AGENT_NAME,
        prompt_file=PROMPT_FILE,
        user_input=user_input,
        history=history,
        temperature=MOVIE_TEMPERATURE,
        max_tokens=MOVIE_MAX_TOKENS,
        empty_input_msg=EMPTY_INPUT_MSG,
    )


# ---------------------------------------------------------------------------
# LangGraph node wrapper
# ---------------------------------------------------------------------------


def movie_agent(state: dict) -> dict:
    """
    LangGraph node — adapts ``get_movie_response`` to the graph's
    ``state in → state out`` interface.

    Reads
    -----
    state["user_input"] : str
    state["history"]    : list[BaseMessage] | None

    Writes
    ------
    state["response"]       : str
    state["selected_agent"] : "movie_agent"
    """
    return {
        **state,
        "response": get_movie_response(
            state.get("user_input", ""),
            history=state.get("history", []),
        ),
        "selected_agent": AGENT_NAME,
    }


__all__ = ["get_movie_response", "movie_agent", "AGENT_NAME"]
