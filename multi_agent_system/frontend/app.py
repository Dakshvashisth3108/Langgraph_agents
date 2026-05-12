"""
frontend/app.py
---------------
Streamlit chat UI for the LangGraph multi-agent system.

Run with:
    streamlit run frontend/app.py

What this file does
===================
1. Renders a modern chat interface (sidebar + chat history + input).
2. Maintains a FULL persistent chat history in ``st.session_state`` —
   every turn the user sees is kept across reruns, complete with the
   agent that handled it and the timestamp.
3. On every user message, calls the compiled LangGraph workflow and
   displays which agent answered + the agent's reply.
4. Catches errors (e.g. Ollama not running) and shows a friendly
   message in the chat instead of a Python traceback.

The code is split into small functions so beginners can read it
top-to-bottom and grow it without untangling one giant block.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Make sure the project root is on sys.path so `from graph.workflow ...`
# works whether Streamlit is launched from the project root or elsewhere.
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from graph.workflow import workflow
from utils.llm import OllamaConnectionError
from utils.logging_setup import setup_logging
from utils.memory import ConversationMemory


# Configure logging once for the whole Streamlit app — safe to call
# multiple times because ``setup_logging`` is idempotent.
setup_logging()


# ---------------------------------------------------------------------------
# Constants — tweak here, not inside the rendering functions.
# ---------------------------------------------------------------------------

APP_TITLE: str = "LangGraph Multi-Agent System"
APP_SUBTITLE: str = "A router decides whether your message goes to MovieAgent or StoryAgent."

USER_ICON: str = "🧑"
ASSISTANT_ICON: str = "🤖"

# Friendly per-agent labels and accent colors for the assistant badges.
# Colors are picked to read well on Streamlit's default light/dark themes.
AGENT_STYLE: dict[str, dict[str, str]] = {
    "movie_agent": {"label": "🎬 MovieAgent", "color": "#7c3aed"},  # purple
    "story_agent": {"label": "📖 StoryAgent", "color": "#0ea5e9"},  # sky-blue
}

# Sidebar config: shown as a simple key-value list.
SIDEBAR_INFO: dict[str, str] = {
    "Active model": "qwen3:8b",
    "Framework": "LangGraph",
    "Backend": "Ollama",
}


# ---------------------------------------------------------------------------
# Page setup — call once, before anything renders.
# ---------------------------------------------------------------------------


def setup_page() -> None:
    """Configure the Streamlit page (title, icon, layout)."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # A pinch of CSS for cleaner chat separation and a polished
    # agent-badge look. Kept tiny on purpose — feel free to delete it
    # if you prefer Streamlit's bare defaults.
    st.markdown(
        """
        <style>
        /* Subtle divider between consecutive chat turns */
        div[data-testid="stChatMessage"] {
            border-bottom: 1px solid rgba(127, 127, 127, 0.12);
            padding-bottom: 0.6rem;
            margin-bottom: 0.6rem;
        }
        /* Agent badge pill */
        .agent-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            color: white;
            margin-bottom: 6px;
        }
        .msg-time {
            font-size: 0.7rem;
            opacity: 0.55;
            margin-left: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session state — Streamlit reruns the whole script on each interaction,
# so anything that should persist (like chat history) lives here.
# ---------------------------------------------------------------------------


def init_session_state() -> None:
    """Create empty containers in session_state on first run."""
    if "messages" not in st.session_state:
        # `messages` is the FULL persistent chat history shown in the UI.
        # Each entry is a dict:
        #   {
        #     "role": "user" | "assistant",
        #     "content": str,
        #     "agent": str | None,       # which agent answered
        #     "timestamp": str,          # "HH:MM" for display
        #   }
        st.session_state.messages = []

    if "memory" not in st.session_state:
        # `memory` is the LangChain-message buffer the LLM actually
        # sees. Kept separate from `messages` because (a) it stores
        # BaseMessage objects, not display dicts, and (b) it is
        # windowed automatically by ConversationMemory.
        st.session_state.memory = ConversationMemory()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar() -> None:
    """Render the sidebar with system info, suggestions, and controls."""
    with st.sidebar:
        st.header("⚙️ System Info")

        for key, value in SIDEBAR_INFO.items():
            st.markdown(f"**{key}**  \n`{value}`")

        st.divider()
        st.subheader("💡 Try asking…")
        st.markdown(
            "- *Tell me the plot of Inception*\n"
            "- *What is the story of Titanic?*\n"
            "- *A robot who learns to paint*\n"
            "- *A tiny dragon afraid of fire*"
        )

        st.divider()

        # ---- Stats -----------------------------------------------------
        total_msgs = len(st.session_state.get("messages", []))
        memory_msgs = len(st.session_state.get("memory", []))
        col_a, col_b = st.columns(2)
        col_a.metric("Chat turns", total_msgs // 2)
        col_b.metric("In memory", memory_msgs)

        st.divider()

        # ---- Controls --------------------------------------------------
        # Clear-chat wipes BOTH the visible history and the LLM-facing memory.
        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.memory.clear()
            st.rerun()

        # Export-chat lets the user download the full transcript as JSON.
        if st.session_state.get("messages"):
            transcript = json.dumps(
                st.session_state.messages,
                indent=2,
                ensure_ascii=False,
            )
            st.download_button(
                label="💾 Download transcript",
                data=transcript,
                file_name="chat_history.json",
                mime="application/json",
                use_container_width=True,
            )

        st.caption("Built with LangGraph + Streamlit")


# ---------------------------------------------------------------------------
# Empty / welcome state
# ---------------------------------------------------------------------------


def render_empty_state() -> None:
    """Friendly placeholder shown before the user sends anything."""
    with st.container():
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 2rem 1rem;
                opacity: 0.85;
            ">
                <h3>👋 Start a new conversation</h3>
                <p>Ask about a <b>movie</b> 🎬 — or share an <b>idea</b> for a short story 📖.<br>
                The router will pick the right agent for you.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Chat history rendering
# ---------------------------------------------------------------------------


def _agent_badge_html(agent_key: str | None) -> str:
    """Return an HTML pill for the agent label, or a neutral default."""
    if agent_key and agent_key in AGENT_STYLE:
        style = AGENT_STYLE[agent_key]
        return (
            f'<span class="agent-badge" style="background:{style["color"]}">'
            f'{style["label"]}</span>'
        )
    return f'<span class="agent-badge" style="background:#6b7280">🤖 {agent_key or "Assistant"}</span>'


def _render_message(msg: dict) -> None:
    """Render one stored message as a chat bubble."""
    role = msg["role"]
    icon = USER_ICON if role == "user" else ASSISTANT_ICON

    with st.chat_message(role, avatar=icon):
        # Header line: agent badge (for assistant) + timestamp on the right.
        header_html = ""
        if role == "assistant":
            header_html += _agent_badge_html(msg.get("agent"))
        ts = msg.get("timestamp")
        if ts:
            header_html += f'<span class="msg-time">{ts}</span>'
        if header_html:
            st.markdown(header_html, unsafe_allow_html=True)

        st.markdown(msg["content"])


def render_chat_history() -> None:
    """Replay every persisted message as a chat bubble."""
    for msg in st.session_state.messages:
        _render_message(msg)


# ---------------------------------------------------------------------------
# Handling a new user message
# ---------------------------------------------------------------------------


def _now_hhmm() -> str:
    """Short 'HH:MM' timestamp string for the message header."""
    return datetime.now().strftime("%H:%M")


def handle_user_message(user_input: str) -> None:
    """
    Run a single chat turn:

      1. Append the user message to persistent history & render it.
      2. Pass current memory + input through the LangGraph workflow.
      3. Append the assistant reply to persistent history & render it.
      4. Update LLM-facing memory.

    The full message dict (role, content, agent, timestamp) is stored
    so the next page rerun replays the conversation exactly as it
    happened — that's what makes the history "persistent".

    Wrapped in try/except so any failure (Ollama down, missing prompt,
    LLM hiccup) shows up as a friendly assistant message instead of
    crashing the page.
    """
    memory: ConversationMemory = st.session_state.memory

    # 1. Persist the user message FIRST, then render it.
    user_msg = {
        "role": "user",
        "content": user_input,
        "agent": None,
        "timestamp": _now_hhmm(),
    }
    st.session_state.messages.append(user_msg)
    _render_message(user_msg)

    # 2. Run the workflow with a spinner inside the assistant bubble.
    agent: str | None
    response: str
    with st.chat_message("assistant", avatar=ASSISTANT_ICON):
        with st.spinner("Thinking…"):
            try:
                result = workflow.invoke(
                    {
                        "user_input": user_input,
                        "history": memory.get_messages(),
                    }
                )
                agent = result.get("selected_agent", "unknown")
                response = result.get("response", "(no response)")
            except OllamaConnectionError as exc:
                agent = None
                response = (
                    f"⚠️ I couldn't reach Ollama.\n\n"
                    f"Please make sure `ollama serve` is running and "
                    f"`qwen3:8b` is pulled, then try again.\n\n"
                    f"_Details: {exc}_"
                )
            except Exception as exc:
                agent = None
                response = f"⚠️ Something went wrong: `{exc}`"

        # 3. Render header (badge + timestamp) and the assistant text.
        ts = _now_hhmm()
        st.markdown(
            _agent_badge_html(agent)
            + f'<span class="msg-time">{ts}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(response)

    # 4. Persist the assistant message into the full chat history.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "agent": agent,
            "timestamp": ts,
        }
    )

    # 5. Update LLM-facing memory only if the turn succeeded — keeps
    #    the buffer clean of error messages.
    if agent:
        memory.add_user_message(user_input)
        memory.add_assistant_message(response)


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def main() -> None:
    """Top-level entry point — Streamlit calls this on every rerun."""
    setup_page()
    init_session_state()

    # Header
    st.title(f"🤖 {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.divider()

    # Sidebar
    render_sidebar()

    # Chat area: replay history, OR show an inviting empty state.
    if st.session_state.messages:
        render_chat_history()
    else:
        render_empty_state()

    # Chat input — Streamlit's modern chat box. The send-arrow on the
    # right acts as the submit button. Pressing Enter also submits.
    user_input = st.chat_input("Ask about a movie or share an idea…")

    if user_input and user_input.strip():
        handle_user_message(user_input.strip())


# Streamlit runs the script top-to-bottom on each interaction, so a
# bare ``main()`` call is the conventional entry point — no
# ``if __name__ == "__main__"`` needed.
main()
