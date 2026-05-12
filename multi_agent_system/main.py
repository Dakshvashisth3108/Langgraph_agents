"""
main.py
-------
Terminal chatbot entry point for the multi-agent system.

What this file does
===================
1. Loads the compiled LangGraph workflow from ``graph/workflow.py``.
2. Starts a friendly REPL loop in the terminal.
3. Sends each user message through the graph.
4. Prints which agent handled the message and what it said.
5. Exits cleanly when the user types ``exit`` or ``quit`` (or hits Ctrl-C).

Run it with:
    python main.py
"""

from __future__ import annotations

import logging
import sys

from graph.workflow import workflow
from utils.llm import OllamaConnectionError
from utils.logging_setup import setup_logging
from utils.memory import ConversationMemory


# ---------------------------------------------------------------------------
# Logging — keep terminal output clean by defaulting to WARNING. Agents
# themselves log at INFO; export LOG_LEVEL=INFO to see those messages.
# ---------------------------------------------------------------------------

setup_logging(level="WARNING")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Terminal formatting helpers
# ---------------------------------------------------------------------------
# Tiny helpers so the loop below stays readable. No external libs needed
# — just plain strings and Unicode box-drawing characters. If your
# terminal doesn't render emojis nicely, feel free to replace them.

LINE = "─" * 64           # thin divider
DOUBLE_LINE = "═" * 64    # heavy divider

EXIT_COMMANDS = {"exit", "quit"}
CLEAR_COMMANDS = {"clear", "reset"}  # wipe memory mid-conversation


def _banner() -> None:
    """Print the welcome message shown once at startup."""
    print(DOUBLE_LINE)
    print("🤖  Multi-Agent AI Chatbot")
    print("    Powered by LangGraph + Ollama (qwen3:8b)")
    print(DOUBLE_LINE)
    print("Ask about a movie  ➜  routed to MovieAgent 🎬")
    print("Share any idea     ➜  routed to StoryAgent 📖")
    print()
    print("Type 'exit' / 'quit' to leave, 'clear' / 'reset' to wipe memory.")
    print("Press Ctrl-C to force quit.")
    print(LINE)


def _print_response(selected_agent: str, response: str) -> None:
    """Pretty-print the agent's reply with a clear separator."""
    # Friendly label per agent — falls back to the raw name if unknown.
    label_map = {
        "movie_agent": "🎬 MovieAgent",
        "story_agent": "📖 StoryAgent",
    }
    label = label_map.get(selected_agent, f"🤖 {selected_agent or 'unknown'}")

    print()
    print(LINE)
    print(f"Agent:    {label}")
    print(LINE)
    print(response.strip() if response else "(no response)")
    print(LINE)
    print()


# ---------------------------------------------------------------------------
# One turn of the conversation
# ---------------------------------------------------------------------------


def _handle_turn(user_input: str, memory: ConversationMemory) -> None:
    """
    Send one user message through the workflow and print the reply.

    Memory flow
    -----------
    1. We snapshot the current history from ``memory`` and pass it
       into the workflow as part of the initial state.
    2. The router routes; the selected specialist reads the history
       from state and injects it into its prompt.
    3. After the workflow returns, we append BOTH the user message
       and the assistant reply to memory — so the *next* turn sees
       the full transcript.

    Any exception is caught here so the chatbot never crashes the
    whole session over a single bad turn.
    """
    try:
        # (1) hand current history to the graph
        result = workflow.invoke(
            {
                "user_input": user_input,
                "history": memory.get_messages(),
            }
        )
    except OllamaConnectionError as exc:
        # Specific, actionable error for the most common setup mistake.
        print(f"\n⚠️  Cannot reach Ollama: {exc}\n")
        return
    except Exception as exc:
        # Last-resort catch-all so the REPL stays alive.
        logger.exception("Workflow failed: %s", exc)
        print(f"\n⚠️  Something went wrong: {exc}\n")
        return

    selected_agent = result.get("selected_agent", "unknown")
    response = result.get("response", "")
    _print_response(selected_agent, response)

    # (3) update memory only after a successful turn
    memory.add_user_message(user_input)
    memory.add_assistant_message(response)


# ---------------------------------------------------------------------------
# Chatbot main loop
# ---------------------------------------------------------------------------


def chat() -> None:
    """Continuously read user input until the user exits."""
    _banner()

    # One memory instance lives for the whole session. It is the
    # "short-term" buffer the prompts read from.
    memory = ConversationMemory()

    while True:
        # 1. Read one line from the user. Catch Ctrl-C / Ctrl-D to exit cleanly.
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            return

        # 2. Skip empty lines so the user can press Enter freely.
        if not user_input:
            continue

        # 3. Check for exit commands.
        if user_input.lower() in EXIT_COMMANDS:
            print("👋 Goodbye!")
            return

        # 4. Check for memory-wipe commands.
        if user_input.lower() in CLEAR_COMMANDS:
            memory.clear()
            print("🧹 Memory cleared.\n")
            continue

        # 5. Otherwise run the full workflow for this turn.
        _handle_turn(user_input, memory)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    try:
        chat()
    except Exception as exc:
        # Belt-and-suspenders: even if `chat()` itself blows up, we exit
        # with a non-zero code and a clean message rather than a Python
        # traceback dump.
        logger.exception("Fatal error in chat loop: %s", exc)
        print(f"\n❌ Fatal error: {exc}")
        sys.exit(1)
