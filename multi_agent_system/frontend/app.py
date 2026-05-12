"""
frontend/app.py
---------------
Streamlit user interface for the multi-agent system.

Run with:
    streamlit run frontend/app.py

The UI is intentionally minimal so beginners can focus on the agent
logic. It calls the compiled `workflow` from `graph/workflow.py` and
displays whatever the chosen agent returns.
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so absolute imports work
# whether Streamlit is launched from the project root or elsewhere.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from graph.workflow import workflow


st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Multi-Agent AI System")
st.caption("Powered by LangGraph + Ollama (qwen3:8b)")

st.markdown(
    "Ask for a **movie recommendation** or a **short story**. "
    "The router will automatically forward your request to the right agent."
)

user_input = st.text_area("Your request", placeholder="e.g. Recommend a thriller movie")

if st.button("Run", type="primary") and user_input.strip():
    with st.spinner("Thinking..."):
        result = workflow.invoke({"user_input": user_input})

    st.success(f"Handled by: `{result.get('agent', 'unknown')}`")
    st.markdown("### Response")
    st.write(result.get("response", "(no response)"))

    with st.expander("Debug: full state"):
        st.json(result)
