"""
agents/movie_agent.py
---------------------
MovieAgent — recommends movies based on user input.

This module exposes a single function `movie_agent(state)` that acts as
a LangGraph node. It:
  1. Reads the user's query from the shared graph state.
  2. Loads the movie prompt template from `prompts/movie_prompt.txt`.
  3. Sends the formatted prompt to the LLM via `utils.llm`.
  4. Returns the response written back into the shared state.
"""

from pathlib import Path
from utils.llm import get_llm

# Resolve the prompt path relative to the project root so that the
# agent works no matter where it is invoked from.
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "movie_prompt.txt"


def _load_prompt() -> str:
    """Read the movie prompt template from disk."""
    return PROMPT_PATH.read_text(encoding="utf-8")


def movie_agent(state: dict) -> dict:
    """
    LangGraph node that produces a movie recommendation.

    Parameters
    ----------
    state : dict
        Shared workflow state. Expected key: `user_input` (str).

    Returns
    -------
    dict
        Updated state with `response` key containing the LLM output.
    """
    user_input = state.get("user_input", "")
    prompt_template = _load_prompt()
    prompt = prompt_template.format(user_input=user_input)

    llm = get_llm(temperature=0.6)
    result = llm.invoke(prompt)

    return {
        **state,
        "response": result.content,
        "agent": "movie_agent",
    }
