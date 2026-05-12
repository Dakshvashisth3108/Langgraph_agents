"""
graph/workflow.py
-----------------
Builds the LangGraph state machine that connects all agents.

Flow
----
    START → router_agent ─┬─► movie_agent ─► END
                          └─► story_agent ─► END

The router decides which branch to take. Adding new agents in the
future = add a new node and a new edge from the router.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.router_agent import router_agent
from agents.movie_agent import movie_agent
from agents.story_agent import story_agent


class GraphState(TypedDict, total=False):
    """
    Shared state object passed between nodes.

    Keys
    ----
    user_input  : the original message from the user
    next_agent  : routing decision, set by router_agent
    response    : final answer produced by a specialist agent
    agent       : which agent produced the response (for debugging)
    """
    user_input: str
    next_agent: str
    response: str
    agent: str


def _route_decision(state: GraphState) -> str:
    """Conditional-edge function: read router's decision from state."""
    return state.get("next_agent", "story_agent")


def build_workflow():
    """
    Compile and return the LangGraph application.

    Call `.invoke({"user_input": "..."})` on the returned object to
    run the full pipeline.
    """
    graph = StateGraph(GraphState)

    # Register nodes.
    graph.add_node("router_agent", router_agent)
    graph.add_node("movie_agent", movie_agent)
    graph.add_node("story_agent", story_agent)

    # Entry point.
    graph.add_edge(START, "router_agent")

    # Conditional branching based on the router's choice.
    graph.add_conditional_edges(
        "router_agent",
        _route_decision,
        {
            "movie_agent": "movie_agent",
            "story_agent": "story_agent",
        },
    )

    # Both specialists end the workflow.
    graph.add_edge("movie_agent", END)
    graph.add_edge("story_agent", END)

    return graph.compile()


# Module-level singleton: import `workflow` directly elsewhere.
workflow = build_workflow()
