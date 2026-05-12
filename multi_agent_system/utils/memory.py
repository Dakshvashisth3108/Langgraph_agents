"""
utils/memory.py
---------------
Short-term conversation memory for the multi-agent system.

What this provides
==================
1. ``ConversationMemory`` — a simple windowed buffer of past messages,
   stored as LangChain ``BaseMessage`` objects (HumanMessage /
   AIMessage). This is the "short-term" memory: it keeps the last
   N messages and drops the oldest ones to stay within budget.

2. ``format_history_for_prompt`` — helper that turns the message list
   into a clean ``User: ...`` / ``Assistant: ...`` transcript that we
   can inject into a prompt template.

Why a custom class instead of ``ConversationBufferMemory``?
-----------------------------------------------------------
The classic ``langchain.memory.*`` helpers are deprecated. The new
idiomatic approach is to keep a plain list of ``BaseMessage`` objects
and use ``langchain_core.messages.trim_messages`` for windowing —
which is exactly what this module does. That keeps us aligned with
LangChain's current direction *and* with LangGraph's
``MessagesState`` pattern (so the same messages flow through both).

Memory flow at a glance
-----------------------
        ┌──────────────────────┐
        │ user types a message │
        └──────────┬───────────┘
                   ▼
       memory.add_user_message(msg)
                   │
                   ▼
   workflow.invoke({"user_input": msg,
                    "history": memory.get_messages()})
                   │
                   ▼
   specialist agent reads `history` from state
   and injects it into the prompt
                   │
                   ▼
       memory.add_assistant_message(reply)
                   │
                   ▼
        next turn sees the new transcript
"""

from __future__ import annotations

import logging
from typing import Iterable

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, trim_messages


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------

# Keep the last N messages (user + assistant turns combined). A small
# window keeps prompts fast and cheap on qwen3:8b — bump this if you
# want the model to remember more.
DEFAULT_MAX_MESSAGES: int = 10


# ---------------------------------------------------------------------------
# ConversationMemory
# ---------------------------------------------------------------------------


class ConversationMemory:
    """
    A tiny FIFO buffer of LangChain messages.

    Usage
    -----
    >>> memory = ConversationMemory()
    >>> memory.add_user_message("hello")
    >>> memory.add_assistant_message("hi there")
    >>> memory.get_messages()
    [HumanMessage(content='hello'), AIMessage(content='hi there')]

    Notes
    -----
    * Stores ``BaseMessage`` objects, so it slots straight into any
      LangChain/LangGraph code that expects messages.
    * Uses ``trim_messages`` after every append, so the list never
      grows beyond ``max_messages``.
    * Holds NO LLM reference — pure data structure. Cheap to create
      and to copy.
    """

    def __init__(self, max_messages: int = DEFAULT_MAX_MESSAGES) -> None:
        self._messages: list[BaseMessage] = []
        self.max_messages: int = max_messages

    # -- mutation ---------------------------------------------------------

    def add_user_message(self, content: str) -> None:
        """Append a user (human) turn and trim if we're over the window."""
        if not content:
            return
        self._messages.append(HumanMessage(content=content))
        self._trim()
        logger.debug("Memory: +user (%d total)", len(self._messages))

    def add_assistant_message(self, content: str) -> None:
        """Append an assistant (AI) turn and trim if we're over the window."""
        if not content:
            return
        self._messages.append(AIMessage(content=content))
        self._trim()
        logger.debug("Memory: +assistant (%d total)", len(self._messages))

    def clear(self) -> None:
        """Wipe all stored messages."""
        self._messages.clear()
        logger.info("Memory cleared.")

    # -- reads ------------------------------------------------------------

    def get_messages(self) -> list[BaseMessage]:
        """Return a COPY of the current message list."""
        # Returning a copy prevents external code from mutating our
        # internal buffer by accident.
        return list(self._messages)

    def __len__(self) -> int:
        return len(self._messages)

    def __bool__(self) -> bool:
        return bool(self._messages)

    # -- internal helpers -------------------------------------------------

    def _trim(self) -> None:
        """Drop oldest messages until we're under the window limit."""
        if len(self._messages) <= self.max_messages:
            return
        # ``trim_messages`` is LangChain's official utility for this.
        # ``token_counter=len`` makes it count messages (not tokens),
        # which matches our "last N messages" semantics.
        self._messages = trim_messages(
            self._messages,
            max_tokens=self.max_messages,
            strategy="last",
            token_counter=len,
            include_system=True,
            allow_partial=False,
        )


# ---------------------------------------------------------------------------
# Prompt formatting helper
# ---------------------------------------------------------------------------


def format_history_for_prompt(messages: Iterable[BaseMessage]) -> str:
    """
    Turn a list of ``BaseMessage`` into a plain transcript string the
    LLM can read.

    Example output::

        User: hello
        Assistant: hi there
        User: tell me a story about a dragon

    Returns an empty string when the list is empty so the prompt
    template renders cleanly on the first turn.
    """
    lines: list[str] = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "User"
        elif isinstance(msg, AIMessage):
            role = "Assistant"
        else:
            role = msg.__class__.__name__.replace("Message", "")
        # ``.content`` can be a list for multimodal messages — we only
        # ever store text, so a str() is safe here.
        lines.append(f"{role}: {str(msg.content).strip()}")
    return "\n".join(lines)


__all__ = [
    "ConversationMemory",
    "format_history_for_prompt",
    "DEFAULT_MAX_MESSAGES",
]
