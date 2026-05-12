# 🤖 LangGraph Multi-Agent System

A **beginner-friendly, production-ready starter** for building multi-agent AI systems in Python.
A central **Router Agent** reads your request and dispatches it to the right specialist — a **Movie Agent** that recommends films or a **Story Agent** that writes short, creative stories — all powered by the **`qwen3:8b`** model running **locally on Ollama** and presented through a clean **Streamlit** UI.

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Architecture](#-architecture)
4. [Folder Structure](#-folder-structure)
5. [Installation Steps](#-installation-steps)
6. [Ollama Setup](#-ollama-setup)
7. [Pulling the qwen3:8b Model](#-pulling-the-qwen38b-model)
8. [Running the Project](#-running-the-project)
9. [Running the Streamlit App](#-running-the-streamlit-app)
10. [Example Inputs & Outputs](#-example-inputs--outputs)
11. [How It Works (Beginner Explanation)](#-how-it-works-beginner-explanation)
12. [Future Improvements](#-future-improvements)
13. [Troubleshooting](#-troubleshooting)
14. [License](#-license)

---

## 🧭 Project Overview

This project demonstrates a **multi-agent workflow** built with **LangGraph** — a library that lets you compose AI agents as nodes in a state graph. Instead of one giant prompt trying to do everything, the work is split between small, focused agents:

| Agent             | Job                                                          |
|-------------------|--------------------------------------------------------------|
| 🚦 Router Agent   | Reads the user's message and picks the right specialist     |
| 🎬 Movie Agent    | Suggests movies based on mood, genre, or interest           |
| 📖 Story Agent    | Writes a short creative story from a user prompt            |

Everything runs **100% locally** — no API keys, no cloud bills — thanks to **Ollama** hosting the `qwen3:8b` open-weights model on your own machine.

---

## ✨ Features

- ✅ **Multi-agent orchestration** with LangGraph
- ✅ **Local LLM** via Ollama (no internet required after setup)
- ✅ **qwen3:8b** — fast, capable 8B-parameter open model
- ✅ **Streamlit UI** with one-click run, debug panel, and state inspector
- ✅ **CLI + REPL** entry point for quick testing
- ✅ **Plain-text prompts** — anyone can edit them, no Python needed
- ✅ **Modular & extensible** — adding a new agent is a 4-step recipe
- ✅ **Single LLM loader** — swap models or providers in one file
- ✅ **Smart routing** — cheap keyword match first, LLM fallback only when needed

---

## 🏗️ Architecture

```
                ┌────────────────┐
   USER ────►   │  Router Agent  │  (decides who handles the request)
                └────────┬───────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌────────────┐         ┌────────────┐
       │ Movie Agent│         │ Story Agent│
       └─────┬──────┘         └─────┬──────┘
             │                      │
             └────────► END ◄───────┘
```

Each agent is a **pure Python function** that receives a `state` dictionary and returns an updated one. LangGraph wires them together into a state machine that the frontend can call with a single `workflow.invoke(...)`.

---

## 📁 Folder Structure

```
multi_agent_system/
│
├── agents/                     # One file per specialist agent
│   ├── __init__.py
│   ├── movie_agent.py          # 🎬 Movie recommender
│   ├── story_agent.py          # 📖 Story writer
│   └── router_agent.py         # 🚦 Routes requests to the right agent
│
├── graph/                      # LangGraph workflow definition
│   ├── __init__.py
│   └── workflow.py             # Builds & compiles the state graph
│
├── prompts/                    # Prompt templates (editable plain text)
│   ├── movie_prompt.txt
│   └── story_prompt.txt
│
├── frontend/                   # Streamlit UI layer
│   ├── __init__.py
│   └── app.py                  # `streamlit run frontend/app.py`
│
├── utils/                      # Shared helpers
│   ├── __init__.py
│   └── llm.py                  # Single place that configures the LLM
│
├── main.py                     # CLI / REPL entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (model, host)
└── README.md                   # You are here 👋
```

**Why this structure?**
- `agents/` keeps each agent isolated → easy to test, easy to add new ones.
- `graph/` holds the orchestration logic, separate from the agents.
- `prompts/` separates *what to say* from *how it runs* → non-developers can tweak.
- `utils/llm.py` is the single source of truth for model config.
- `frontend/` is decoupled — you could swap Streamlit for FastAPI without touching the agents.

---

## 🛠️ Installation Steps

### Prerequisites
- **Python 3.10+** — verify with `python --version`
- **pip** and **venv** (ship with modern Python)
- **~6 GB free disk space** for the qwen3:8b model
- **8 GB+ RAM** recommended (16 GB ideal)

### Step 1 — Clone the repository
```bash
git clone <your-repo-url>
cd multi_agent_system
```

### Step 2 — Create a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should now see `(.venv)` at the start of your terminal prompt.

### Step 3 — Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` installs the **minimum compatible set**:

| Package               | Purpose                                |
|-----------------------|----------------------------------------|
| `langgraph`           | Multi-agent state machine orchestration|
| `langchain`           | Core LLM framework                     |
| `langchain-community` | Community integrations / utilities     |
| `langchain-ollama`    | Connects LangChain to Ollama           |
| `streamlit`           | Web UI                                 |
| `python-dotenv`       | Loads `.env` config at runtime         |

### Step 4 — Verify installation
```bash
python -c "import langgraph, langchain, streamlit; print('OK')"
```
You should see `OK`.

---

## 🦙 Ollama Setup

[Ollama](https://ollama.com) is the runtime that hosts the `qwen3:8b` model locally on your machine. Think of it as a tiny server for LLMs.

### Install Ollama

| OS         | Install command / link                                 |
|------------|--------------------------------------------------------|
| **Windows**| Download installer from <https://ollama.com/download>  |
| **macOS**  | Download from <https://ollama.com/download> *or* `brew install ollama` |
| **Linux**  | `curl -fsSL https://ollama.com/install.sh \| sh`       |

### Start the Ollama server
Open a **new terminal** and run:
```bash
ollama serve
```
Leave this terminal open — it must keep running while you use the project. Ollama listens on `http://localhost:11434` by default (this matches `OLLAMA_BASE_URL` in `.env`).

### Verify Ollama is running
```bash
curl http://localhost:11434
# → "Ollama is running"
```

---

## 📥 Pulling the qwen3:8b Model

In a separate terminal (not the one running `ollama serve`), pull the model:
```bash
ollama pull qwen3:8b
```

This downloads the model (~5 GB). It happens **once** — afterwards the model lives on your disk forever.

### Verify the model is installed
```bash
ollama list
```
You should see `qwen3:8b` in the list.

### Quick smoke test
```bash
ollama run qwen3:8b "Hello, are you working?"
```
If you get a reply, you're ready to run the project. Type `/bye` to exit the chat.

---

## ▶️ Running the Project

### Option A — Command line (fastest)
```bash
python main.py "Recommend a feel-good movie"
python main.py "Tell me a short story about a robot who learns to paint"
```

### Option B — Interactive REPL
```bash
python main.py
```
You'll get a prompt where you can chat back and forth. Type `exit` or `quit` to leave.

### Option C — Streamlit web app
See the next section ⬇️

---

## 🎨 Running the Streamlit App

With your virtual environment activated **and** `ollama serve` running:

```bash
streamlit run frontend/app.py
```

Streamlit will:
1. Open <http://localhost:8501> in your default browser
2. Show a text box where you can type any request
3. Run your request through the LangGraph workflow
4. Display the response along with which agent handled it
5. Provide an expandable **Debug** panel showing the full state dict

**Stop the app** with `Ctrl + C` in the terminal.

---

## 💬 Example Inputs & Outputs

### Example 1 — Movie Recommendation
**Input:**
```
Recommend a feel-good movie for a rainy Sunday
```

**Routing:** `router_agent` detects the keyword `movie` → forwards to `movie_agent`.

**Output (sample):**
```
[Handled by: movie_agent]

1. The Secret Life of Walter Mitty (2013, Adventure/Comedy)
   A daydreamer's quiet life turns into a real-world adventure — visually
   stunning and uplifting from start to finish.

2. Chef (2014, Comedy/Drama)
   A father reconnects with his son through a food-truck road trip.
   Warm, funny, and packed with great food shots.

3. Paddington 2 (2017, Family/Comedy)
   Charming, hilarious, and impossibly kind — perfect for a rainy day.
```

---

### Example 2 — Short Story
**Input:**
```
Write me a short story about a lighthouse keeper who befriends a whale
```

**Routing:** `router_agent` detects the keyword `story` → forwards to `story_agent`.

**Output (sample):**
```
[Handled by: story_agent]

For thirty years, Old Tomas had lit the lamp at Cape Solitude. The cliffs
knew his footsteps, the gulls knew his name, and the sea — vast and grey
— had always kept its distance.

Until the night the great blue whale came.

She arrived during a storm, beaching herself in the cove below the
lighthouse. Tomas worked through the night, hauling buckets of seawater
over her enormous flank, whispering to her as if she were a child. By
dawn the tide had returned, and so had she — to the deep.

But every evening after, when Tomas lit the lamp, a spout of mist would
rise from the dark water below. A signal. A thank-you. A friend.

He never felt alone at Cape Solitude again.
```

---

### Example 3 — Ambiguous Input (LLM Fallback Routing)
**Input:**
```
Surprise me with something creative
```

**Routing:** No keyword match → router falls back to LLM classification → picks `story_agent`.

**Output (sample):**
```
[Handled by: story_agent]

(a short creative story...)
```

---

## 🧑‍🎓 How It Works (Beginner Explanation)

### What's an "agent"?
In this project, an agent is just a **Python function** that:
1. Receives a small dictionary called `state`.
2. Asks the LLM to do something (e.g. *"recommend a movie"*).
3. Puts the LLM's reply back into the dictionary.
4. Returns the updated dictionary.

That's it. No magic, no classes, no inheritance — just functions.

### What does LangGraph add?
LangGraph lets you **connect** these agent-functions into a flowchart:
- Nodes = your agent functions.
- Edges = "after this node, go to that node".
- Conditional edges = "after this node, look at the state and pick the next node dynamically."

The Router Agent uses a **conditional edge**: it writes `next_agent` into the state, and LangGraph reads that value to decide where to go next.

### Why a "Router"?
Without a router, you'd have to write `if/else` code in your UI for every new specialist. With a router agent, the logic lives **inside the graph** — your UI just calls `workflow.invoke(...)` and gets an answer. To add a music recommender tomorrow, you change the graph and the router, **never** the frontend.

### Why Ollama and qwen3:8b?
- **Ollama** is the easiest way to run an LLM on your own computer.
- **qwen3:8b** is a strong open-weights model that fits on most modern laptops — it's fast enough for interactive use and capable enough to produce quality responses.
- Running locally means **no API costs, no rate limits, no data leaving your machine**.

### Why Streamlit?
Streamlit lets you build a real web UI in ~30 lines of Python — perfect for getting an AI prototype in front of users without learning HTML/CSS/JavaScript.

---

## 🚀 Future Improvements

This project is intentionally minimal so you can grow it in any direction. Some ideas:

### Easy wins
- 🎵 **Add a Music Agent** that recommends songs or playlists.
- 📚 **Add a Book Agent** for reading recommendations.
- 🌐 **Add a Translator Agent** that detects language and translates.
- 🔍 **Add chat history** so the agent remembers previous turns.

### Intermediate
- 🧠 **Memory layer** — give agents long-term memory using a vector store (e.g. Chroma, FAISS).
- 🛠️ **Tool use** — let agents call functions (search the web, query a database, run Python).
- 🔁 **Multi-step workflows** — chain agents so one's output becomes another's input.
- 🧪 **Unit tests** for each agent + integration tests for the graph.
- 📊 **LangSmith tracing** — toggle the existing `.env` flags to see every LLM call in a dashboard.

### Advanced
- 🤝 **Human-in-the-loop** — pause the graph and ask the user to approve risky steps.
- 🔂 **Self-correcting loops** — let a "critic" agent review and re-run the specialist if quality is low.
- 🌍 **REST API** — wrap the graph with FastAPI and deploy.
- 🐳 **Dockerize** Ollama + the app for one-command deployment.
- 🎙️ **Voice input/output** with Whisper + a TTS model.

---

## 🩹 Troubleshooting

| Problem                                       | Fix                                                              |
|-----------------------------------------------|------------------------------------------------------------------|
| `ConnectionError: localhost:11434`            | Ollama is not running — start it with `ollama serve`.            |
| `model 'qwen3:8b' not found`                  | Run `ollama pull qwen3:8b`.                                      |
| `ModuleNotFoundError: No module named ...`    | Activate the virtual environment, then `pip install -r requirements.txt`. |
| Streamlit page is blank / errors on launch    | Make sure you ran it from the project root: `streamlit run frontend/app.py`. |
| First response is very slow                   | Normal — Ollama loads the model into RAM on first call. Subsequent calls are fast. |
| Out-of-memory errors                          | qwen3:8b needs ~6 GB RAM. Close other apps or try a smaller model like `qwen3:4b`. |
| Router picks the wrong agent                  | Edit the keyword lists in [`agents/router_agent.py`](agents/router_agent.py) or refine the LLM fallback prompt. |

---

## 📜 License

MIT — free to use, modify, and learn from. Build something amazing! ✨

---

> Made with ❤️ for anyone learning multi-agent AI systems.
> If this helped you, consider sharing the repo or contributing a new agent.
