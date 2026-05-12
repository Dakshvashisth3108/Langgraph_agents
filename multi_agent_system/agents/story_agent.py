"""
agents/story_agent.py
---------------------
StoryAgent — generates short creative stories from a user prompt.

Like every other agent in this project, it is a plain Python function
that takes a `state` dict (from LangGraph) and returns an updated
`state` dict. Keeping agents as simple functions makes them easy to
test in isolation and easy to wire into the graph.
"""

from pathlib import Path
from utils.llm import get_llm

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "story_prompt.txt"


def _load_prompt() -> str:
    """Read the story prompt template from disk."""
    return PROMPT_PATH.read_text(encoding="utf-8")


def story_agent(state: dict) -> dict:
    """
    LangGraph node that produces a short story.

    Parameters
    ----------
    state : dict
        Shared workflow state. Expected key: `user_input` (str).

    Returns
    -------
    dict
        Updated state with the story stored in `response`.
    """
    user_input = state.get("user_input", "")
    prompt_template = _load_prompt()
    prompt = prompt_template.format(user_input=user_input)

    # Higher temperature → more creative storytelling.
    llm = get_llm(temperature=0.9)
    result = llm.invoke(prompt)

    return {
        **state,
        "response": result.content,
        "agent": "story_agent",
    }
