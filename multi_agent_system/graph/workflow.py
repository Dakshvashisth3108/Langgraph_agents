"""
graph/workflow.py
-----------------
LangGraph workflow that wires the three agents together.

Execution flow
==============

    ┌──────┐
    │START │
    └──┬───┘
       │      (1) user_input enters the graph in `state`
       ▼
    ┌──────────────┐
    │ router_agent │  (2) sets state["selected_agent"]
    └──────┬───────┘
           │
           │  (3) conditional edge reads state["selected_agent"]
           ▼
    ┌───────────────┐          ┌───────────────┐
    │ movie_agent   │   OR     │ story_agent   │
    └──────┬────────┘          └──────┬────────┘
           │  (4) writes state["response"]
           ▼                          ▼
                       ┌──────┐
                       │ END  │  (5) final state is returned to caller
                       └──────┘

Each node in the graph is a plain Python function that takes a state
dictionary and returns an updated one. LangGraph stitches them
together into a directed graph and exposes a single entry point
(``workflow.invoke({...})``) for the frontend / CLI to call.

Adding a new specialist (e.g. a music_agent) is a four-step recipe:
    1. Add a keyword tuple + dispatch branch in agents/router_agent.py
    2. Register the new node with ``graph.add_node(...)`` below
    3. Add an entry to the conditional-edge mapping below
    4. Add ``graph.add_edge("music_agent", END)``
"""

from __future__ import annotations

import logging
from typing import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph

from agents.movie_agent import movie_agent
from agents.router_agent import MOVIE_AGENT, STORY_AGENT, router_agent
from agents.story_agent import story_agent


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared state schema
# ---------------------------------------------------------------------------


class GraphState(TypedDict, total=False):
    """
    Shared state passed between nodes during a single workflow run.

    Fields
    ------
    user_input : str
        The original message the user typed. Set by the caller of
        ``workflow.invoke(...)`` and never modified by the agents.
    selected_agent : str
        Filled in by the router. One of ``"movie_agent"`` or
        ``"story_agent"``. Used by LangGraph to pick the next node.
    response : str
        The final answer produced by whichever specialist handled the
        request. This is what the UI / CLI displays to the user.
    history : list[BaseMessage]
        Short-term conversation memory — past Human/AI messages from
        earlier turns. The caller (CLI or Streamlit app) is in charge
        of maintaining this list across invocations via a
        ``ConversationMemory`` instance from ``utils.memory``.
        Specialist agents read this and inject it into their prompts
        so the model can answer follow-ups in context.

    ``total=False`` means every field is optional at any single moment
    — fields fill in as the graph executes. By the time the workflow
    finishes, all four should be populated.
    """

    user_input: str
    selected_agent: str
    response: str
    history: list[BaseMessage]


# ---------------------------------------------------------------------------
# Conditional-edge function
# ---------------------------------------------------------------------------


def _route_decision(state: GraphState) -> str:
    """
    Read the router's choice out of the state.

    LangGraph calls this right after the router node finishes; whatever
    string we return is matched against the conditional-edge mapping
    below to pick the next node.

    Defaults to STORY_AGENT if ``selected_agent`` is somehow missing,
    so the graph never gets stuck on malformed input.
    """
    choice = state.get("selected_agent", STORY_AGENT)
    logger.debug("Conditional edge → %s", choice)
    return choice


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------


def build_workflow():
    """
    Construct, wire, and compile the LangGraph application.

    Returns
    -------
    Compiled LangGraph
        Call ``.invoke({"user_input": "..."})`` on it to run the
        full pipeline. The returned dict is the final state.
    """
    logger.info("Building LangGraph workflow…")

    # 1. Create the graph object with our state schema.
    graph = StateGraph(GraphState)

    # 2. Register the three nodes. Each is a plain function:
    #    `state in → state out`.
    graph.add_node("router_agent", router_agent)
    graph.add_node(MOVIE_AGENT, movie_agent)
    graph.add_node(STORY_AGENT, story_agent)

    # 3. The graph always starts at the router.
    graph.add_edge(START, "router_agent")

    # 4. After the router runs, branch based on what it wrote into
    #    state["selected_agent"]. The third argument is a mapping:
    #        decision-string  →  next-node-name.
    graph.add_conditional_edges(
        "router_agent",
        _route_decision,
        {
            MOVIE_AGENT: MOVIE_AGENT,
            STORY_AGENT: STORY_AGENT,
        },
    )

    # 5. Both specialists end the workflow — there's nothing after them.
    graph.add_edge(MOVIE_AGENT, END)
    graph.add_edge(STORY_AGENT, END)

    # 6. Compile turns the declarative graph into an executable object.
    #    Always call .compile() before .invoke().
    compiled = graph.compile()
    logger.info("Workflow compiled successfully.")
    return compiled


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
#
# Compile the graph once at import time so callers can simply do
#     from graph.workflow import workflow
#     workflow.invoke({"user_input": "..."})
#
# Note: this does NOT instantiate the LLM. ``get_llm()`` is only called
# the first time a specialist node actually runs, so importing this
# module is cheap and safe even when Ollama is offline.

workflow = build_workflow()


__all__ = ["workflow", "build_workflow", "GraphState"]
