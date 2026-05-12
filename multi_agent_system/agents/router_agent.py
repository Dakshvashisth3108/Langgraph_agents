"""
agents/router_agent.py
----------------------
RouterAgent — decides which specialist agent should handle the query.

The router is the "traffic cop" of the system. It inspects the user
input and returns a string label that LangGraph uses to pick the next
node in the workflow. Adding a new specialist (e.g. `music_agent`) is
as simple as:
    1. Add another keyword branch (or extend the LLM classifier).
    2. Register the new agent in `graph/workflow.py`.
"""

from utils.llm import get_llm


# Keep keyword lists at module level so they're easy to edit / extend.
MOVIE_KEYWORDS = ("movie", "film", "cinema", "watch", "actor", "actress")
STORY_KEYWORDS = ("story", "tale", "narrate", "write me", "once upon")


def _keyword_route(user_input: str) -> str | None:
    """Cheap rule-based routing — returns None if no keyword matches."""
    text = user_input.lower()
    if any(k in text for k in MOVIE_KEYWORDS):
        return "movie_agent"
    if any(k in text for k in STORY_KEYWORDS):
        return "story_agent"
    return None


def _llm_route(user_input: str) -> str:
    """Fallback: ask the LLM to classify when keywords don't match."""
    llm = get_llm(temperature=0.0)
    prompt = (
        "You are a router. Read the user message and reply with EXACTLY "
        "one word: either `movie_agent` (if the user wants a movie "
        "recommendation) or `story_agent` (if the user wants a story).\n\n"
        f"User message: {user_input}\n\nAnswer:"
    )
    decision = llm.invoke(prompt).content.strip().lower()

    # Defensive: if the model hallucinates a label, default to story_agent.
    if "movie" in decision:
        return "movie_agent"
    return "story_agent"


def router_agent(state: dict) -> dict:
    """
    LangGraph node that picks the next agent.

    Parameters
    ----------
    state : dict
        Shared workflow state. Expected key: `user_input` (str).

    Returns
    -------
    dict
        State updated with `next_agent` key set to either
        `"movie_agent"` or `"story_agent"`.
    """
    user_input = state.get("user_input", "")

    next_agent = _keyword_route(user_input) or _llm_route(user_input)

    return {
        **state,
        "next_agent": next_agent,
    }
