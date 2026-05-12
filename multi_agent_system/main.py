"""
main.py
-------
Command-line entry point for the multi-agent system.

Usage:
    python main.py "Recommend a sci-fi movie"
    python main.py "Tell me a funny story about a cat"

If no argument is provided, an interactive REPL is started.
This file is useful for quick testing without launching Streamlit.
"""

import sys
from graph.workflow import workflow


def run_once(user_input: str) -> None:
    """Run the workflow a single time and print the result."""
    result = workflow.invoke({"user_input": user_input})
    print(f"\n[Handled by: {result.get('agent', 'unknown')}]\n")
    print(result.get("response", "(no response)"))
    print()


def repl() -> None:
    """Simple read-eval-print loop for quick testing."""
    print("Multi-Agent System REPL (type 'exit' to quit)\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            return
        if not user_input:
            continue
        run_once(user_input)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_once(" ".join(sys.argv[1:]))
    else:
        repl()
