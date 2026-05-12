"""
agents/router_agent.py
----------------------
RouterAgent — an LLM-powered intent classifier.

This module exposes two complementary functions:

1. ``route_query(user_input, history=None)``
     Standalone helper. Inspects the user's message, picks the right
     specialist agent, calls it, and returns BOTH the agent's name and
     its generated response in a single dictionary.

2. ``router_agent(state)``
     LangGraph node. Looks at the user input and conversation history,
     writes the chosen specialist's name into ``state["selected_agent"]``,
     and lets LangGraph's conditional edges dispatch to that node.

How routing works (LLM-first, confidence-gated, with a safety net)
==================================================================
For every query, the router:

  1. Sends the user message (plus the recent conversation history) to
     **qwen3:8b** with a tiny classification prompt that asks for a
     JSON object: ``{"agent": ..., "confidence": ..., "reason": ...}``.

  2. Parses the JSON. If the LLM returns a clean answer with a
     confidence at or above ``CONFIDENCE_THRESHOLD``, that's the
     decision — even if the message contains no obvious "movie" word.
     This is how follow-ups like *"what else has that director made?"*
     correctly land at MovieAgent.

  3. If the LLM's confidence is **below** the threshold the router
     defaults to ``STORY_AGENT`` — the story agent can gracefully
     handle anything, so it's the safer fallback for ambiguous input.

  4. If the LLM call fails entirely (Ollama down, unparseable output,
     etc.) the router falls back to a tiny keyword check. This is a
     SAFETY NET, not the primary mechanism — it only fires when the
     LLM is unavailable.

So the rule is:  LLM intent → confidence gate → keyword fallback.
We never rely on keywords alone.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from langchain_core.messages import BaseMessage

from agents.movie_agent import get_movie_response
from agents.story_agent import generate_story
from utils.llm import OllamaConnectionError, get_llm
from utils.memory import format_history_for_prompt


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Canonical agent labels
# ---------------------------------------------------------------------------
# Kept as constants so the rest of the code never types raw strings —
# catches typos at lint time and makes adding a new agent a one-place edit.

MOVIE_AGENT: str = "movie_agent"
STORY_AGENT: str = "story_agent"


# ---------------------------------------------------------------------------
# Classifier tuning
# ---------------------------------------------------------------------------

# Temperature 0 → deterministic classification. We do NOT want the
# router being creative — same query should always route the same way.
ROUTER_TEMPERATURE: float = 0.0

# Tiny output budget — the JSON we want is ~60 tokens max.
ROUTER_MAX_TOKENS: int = 120

# Confidence below this threshold → defer to the safe default
# (STORY_AGENT). Tune up for stricter routing, down to trust the LLM
# more.
CONFIDENCE_THRESHOLD: float = 0.60

# Last-resort keyword hints used ONLY when the LLM is unreachable.
# These are not the primary routing mechanism — they exist so the app
# still works if Ollama crashes mid-session.
MOVIE_KEYWORDS_FALLBACK: tuple[str, ...] = (
    "movie",
    "film",
    "plot",
    "story of",
    "cinema",
)


# ---------------------------------------------------------------------------
# Classification prompt
# ---------------------------------------------------------------------------
# Kept short on purpose — small prompts are cheaper and easier for the
# 8B model to follow exactly. Note the doubled braces in the JSON
# example: required because we use ``str.format`` below.

CLASSIFIER_PROMPT_TEMPLATE = """You are a routing classifier in a multi-agent system.

Decide which specialist should handle the user's latest message:

- "movie_agent": user is asking about a SPECIFIC film — its plot, story,
   characters, director, release year, cast, summary, or follow-up
   questions about a movie discussed earlier.
- "story_agent": user wants you to GENERATE a creative/imaginative story,
   narrative, or fictional text from an idea, OR the request is general
   and doesn't fit movie_agent.

Conversation so far (may be empty):
{history}

Latest user message: "{user_input}"

Respond with EXACTLY one line of JSON (no markdown fences, no extra text):
{{"agent": "movie_agent" or "story_agent", "confidence": 0.0 to 1.0, "reason": "one short sentence"}}

JSON:"""


# ---------------------------------------------------------------------------
# JSON extraction helper
# ---------------------------------------------------------------------------


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json_object(raw: str) -> dict[str, Any] | None:
    """
    Pull the first ``{...}`` JSON object out of an LLM response.

    Local models sometimes wrap output in markdown fences or add extra
    chatter before/after the JSON. This helper finds the first balanced
    object and parses it.

    Returns ``None`` if no parseable object is found — caller decides
    what to do (we fall back to keywords).
    """
    if not raw:
        return None

    # Strip leading ```json / ``` fences if present.
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        # Drop a leading "json" hint if the fence was ```json ... ```
        text = re.sub(r"^json\s*", "", text, flags=re.IGNORECASE).strip()

    # Try the whole string first (the cheap path).
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Otherwise scan for the first {...} block.
    match = _JSON_OBJECT_RE.search(text)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _llm_classify(
    user_input: str,
    history: list[BaseMessage] | None,
) -> dict[str, Any] | None:
    """
    Ask the LLM to classify the user's intent.

    Returns
    -------
    dict | None
        ``{"agent": ..., "confidence": float, "reason": str}`` on
        success, or ``None`` if the LLM is unreachable or its output
        cannot be parsed (caller falls back to keywords).
    """
    history_text = format_history_for_prompt(history or [])
    prompt = CLASSIFIER_PROMPT_TEMPLATE.format(
        history=history_text or "(no prior turns)",
        user_input=user_input,
    )

    try:
        llm = get_llm(
            temperature=ROUTER_TEMPERATURE,
            max_tokens=ROUTER_MAX_TOKENS,
        )
        raw = llm.invoke(prompt).content
    except OllamaConnectionError as exc:
        logger.warning("Router LLM unreachable, will use keyword fallback: %s", exc)
        return None
    except Exception as exc:
        # Defensive: any other LLM error → fallback.
        logger.exception("Router LLM call failed: %s", exc)
        return None

    parsed = _extract_json_object(str(raw))
    if parsed is None:
        logger.warning("Router LLM returned unparseable output: %r", raw)
        return None

    # Validate and normalise the fields.
    agent = str(parsed.get("agent", "")).strip().lower()
    if agent not in (MOVIE_AGENT, STORY_AGENT):
        logger.warning("Router LLM returned unknown agent label: %r", agent)
        return None

    try:
        confidence = float(parsed.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))  # clamp to [0, 1]

    reason = str(parsed.get("reason", "")).strip()

    return {"agent": agent, "confidence": confidence, "reason": reason}


def _keyword_fallback(user_input: str) -> str:
    """
    Tiny safety net used ONLY when the LLM classifier is unavailable.

    Returns ``MOVIE_AGENT`` if any of the fallback keywords appear in
    the message, otherwise ``STORY_AGENT``.
    """
    text = (user_input or "").lower()
    for keyword in MOVIE_KEYWORDS_FALLBACK:
        if keyword in text:
            logger.debug("Fallback keyword '%s' matched", keyword)
            return MOVIE_AGENT
    return STORY_AGENT


def _classify(
    user_input: str,
    history: list[BaseMessage] | None = None,
) -> str:
    """
    Top-level routing decision. LLM-first with confidence gating and
    a keyword safety net.

    Returns either ``MOVIE_AGENT`` or ``STORY_AGENT``.
    """
    # 1. Try the LLM classifier.
    classification = _llm_classify(user_input, history)

    # 2. LLM failed → fall back to keyword check.
    if classification is None:
        chosen = _keyword_fallback(user_input)
        logger.info("Router → %s (via keyword fallback)", chosen)
        return chosen

    # 3. Confidence too low → safer default (StoryAgent can handle anything).
    if classification["confidence"] < CONFIDENCE_THRESHOLD:
        logger.info(
            "Router → %s (low confidence %.2f, defaulting from suggested %s) | %s",
            STORY_AGENT,
            classification["confidence"],
            classification["agent"],
            classification["reason"],
        )
        return STORY_AGENT

    # 4. Confident LLM decision wins.
    chosen = classification["agent"]
    logger.info(
        "Router → %s (LLM confidence %.2f) | %s",
        chosen,
        classification["confidence"],
        classification["reason"],
    )
    return chosen


def _dispatch(
    agent_name: str,
    user_input: str,
    history: list[BaseMessage] | None,
) -> str:
    """Call the specialist agent identified by ``agent_name``."""
    if agent_name == MOVIE_AGENT:
        return get_movie_response(user_input, history=history)
    # Default branch handles STORY_AGENT (and any future fallback).
    return generate_story(user_input, history=history)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def route_query(
    user_input: str,
    history: list[BaseMessage] | None = None,
) -> dict:
    """
    Route a user query to the right specialist and return the result.

    Parameters
    ----------
    user_input : str
        Whatever the user typed.
    history : list[BaseMessage] | None
        Optional short-term memory from ``utils.memory``. Improves
        routing on follow-up questions like "what about the sequel?".

    Returns
    -------
    dict
        ``{"agent": <agent name>, "response": <agent's reply>}``.
        On empty input, returns a polite prompt back to the user.
    """
    # 1. Guard against empty input — saves a model call.
    if not user_input or not user_input.strip():
        logger.warning("route_query called with empty input")
        return {
            "agent": None,
            "response": "Please type something — a movie name, an idea, anything!",
        }

    # 2. Decide which agent should handle this query (LLM-driven).
    agent_name = _classify(user_input, history)

    # 3. Dispatch and capture the specialist's reply. Specialists do
    #    their own error handling, so `response` is always a string.
    response = _dispatch(agent_name, user_input, history)

    return {"agent": agent_name, "response": response}


# ---------------------------------------------------------------------------
# LangGraph node wrapper
# ---------------------------------------------------------------------------


def router_agent(state: dict) -> dict:
    """
    LangGraph routing node — sets ``selected_agent`` in the shared state.

    Unlike ``route_query`` (which calls the specialist itself), this
    node only *decides*. LangGraph's conditional edges then dispatch
    to the chosen specialist node.

    Reads
    -----
    state["user_input"] : str — required
    state["history"]    : list[BaseMessage] — optional, used for
                          smarter follow-up routing

    Writes
    ------
    state["selected_agent"] : "movie_agent" or "story_agent"
    """
    user_input = state.get("user_input", "")
    history = state.get("history", [])
    selected = _classify(user_input, history)

    return {
        **state,
        "selected_agent": selected,
    }


__all__ = [
    "route_query",
    "router_agent",
    "MOVIE_AGENT",
    "STORY_AGENT",
    "CONFIDENCE_THRESHOLD",
]
