"""
agents/story_agent.py
---------------------
StoryAgent — a creative storyteller that turns an idea into a short story.

Public API
----------
* ``generate_story(user_input, history=None) -> str``
    Standalone helper for scripts, tests, REPLs.
* ``story_agent(state) -> dict``
    LangGraph node wrapper used by ``graph/workflow.py``.

The shared prompt-loading / LLM-calling / error-handling logic lives
in :mod:`agents._base`. This file only configures a story-flavoured
call to that pipeline.
"""

from __future__ import annotations

from langchain_core.messages import BaseMessage

from agents._base import run_agent


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AGENT_NAME: str = "story_agent"
PROMPT_FILE: str = "story_prompt.txt"

# High temperature → varied, imaginative storytelling.
# Token budget sized for a ~300-word story (≈400-500 tokens) with a buffer.
STORY_TEMPERATURE: float = 0.9
STORY_MAX_TOKENS: int = 800

EMPTY_INPUT_MSG: str = "Please share a sentence or idea, and I'll write a story for you."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_story(
    user_input: str,
    history: list[BaseMessage] | None = None,
) -> str:
    """
    Turn a sentence or idea into a short creative story.

    Parameters
    ----------
    user_input : str
        A scenario or idea (e.g. "a robot who learns to paint").
    history : list[BaseMessage] | None
        Past conversation messages, enabling follow-ups like
        "continue that story" or "make it sadder".

    Returns
    -------
    str
        A short (~200-300 word) story; or a friendly error message
        if something failed.
    """
    return run_agent(
        agent_name=AGENT_NAME,
        prompt_file=PROMPT_FILE,
        user_input=user_input,
        history=history,
        temperature=STORY_TEMPERATURE,
        max_tokens=STORY_MAX_TOKENS,
        empty_input_msg=EMPTY_INPUT_MSG,
    )


# ---------------------------------------------------------------------------
# LangGraph node wrapper
# ---------------------------------------------------------------------------


def story_agent(state: dict) -> dict:
    """
    LangGraph node — adapts ``generate_story`` to the graph's
    ``state in → state out`` interface.

    Reads
    -----
    state["user_input"] : str
    state["history"]    : list[BaseMessage] | None

    Writes
    ------
    state["response"]       : str
    state["selected_agent"] : "story_agent"
    """
    return {
        **state,
        "response": generate_story(
            state.get("user_input", ""),
            history=state.get("history", []),
        ),
        "selected_agent": AGENT_NAME,
    }


__all__ = ["generate_story", "story_agent", "AGENT_NAME"]
