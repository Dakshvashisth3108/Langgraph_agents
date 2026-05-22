// Builds LangGraph_Multi_Agent_System.pptx
// Theme: dark navy/slate with purple (movie) + sky-blue (story) accents.

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Daksh Vashisth";
pres.title = "LangGraph Multi-Agent System";
pres.subject = "Architecture, implementation, and tech stack overview";

const C = {
  bg: "0F172A", bg2: "1E293B", bg3: "334155",
  card: "1E293B", border: "475569",
  purple: "7C3AED", purpleSoft: "A78BFA",
  sky: "0EA5E9", skySoft: "7DD3FC",
  emerald: "10B981", amber: "F59E0B", rose: "F43F5E",
  text: "F1F5F9", textBody: "CBD5E1", textMuted: "94A3B8",
  white: "FFFFFF",
};
const F = { head: "Calibri", body: "Calibri", mono: "Consolas" };

function setDarkBg(slide) { slide.background = { color: C.bg }; }

function addHeader(slide, title, kicker) {
  slide.addShape(pres.shapes.OVAL, {
    x: 0.6, y: 0.55, w: 0.18, h: 0.18,
    fill: { color: C.purple }, line: { color: C.purple },
  });
  slide.addShape(pres.shapes.OVAL, {
    x: 0.82, y: 0.55, w: 0.18, h: 0.18,
    fill: { color: C.sky }, line: { color: C.sky },
  });
  if (kicker) {
    slide.addText(kicker.toUpperCase(), {
      x: 1.1, y: 0.5, w: 6, h: 0.3,
      fontSize: 11, fontFace: F.head, bold: true,
      color: C.textMuted, charSpacing: 4, margin: 0,
    });
  }
  slide.addText(title, {
    x: 0.6, y: 0.85, w: 12.1, h: 0.8,
    fontSize: 32, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
}

function addFooter(slide, pageNumber, total) {
  slide.addShape(pres.shapes.LINE, {
    x: 0.6, y: 7.05, w: 12.1, h: 0,
    line: { color: C.border, width: 0.75 },
  });
  slide.addText("LangGraph Multi-Agent System  ·  Daksh Vashisth", {
    x: 0.6, y: 7.15, w: 8, h: 0.3,
    fontSize: 9, fontFace: F.body, color: C.textMuted, margin: 0,
  });
  slide.addText(`${pageNumber} / ${total}`, {
    x: 11.5, y: 7.15, w: 1.2, h: 0.3,
    fontSize: 9, fontFace: F.body, color: C.textMuted, align: "right", margin: 0,
  });
}

function card(slide, opts) {
  const { x, y, w, h, accent, fill = C.card } = opts;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: fill },
    line: { color: C.border, width: 0.5 },
    shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.25 },
  });
  if (accent) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.08, h,
      fill: { color: accent }, line: { color: accent },
    });
  }
}

function pill(slide, x, y, label, color, textColor = C.white) {
  const w = Math.max(0.9, 0.18 * label.length);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h: 0.36,
    fill: { color }, line: { color }, rectRadius: 0.18,
  });
  slide.addText(label, {
    x, y, w, h: 0.36,
    fontSize: 11, fontFace: F.head, bold: true,
    color: textColor, align: "center", valign: "middle", margin: 0,
  });
  return w;
}

// SLIDE 1 — Title
function slideTitle(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  s.addShape(pres.shapes.OVAL, {
    x: -2.5, y: -2.5, w: 7, h: 7,
    fill: { color: C.purple, transparency: 80 }, line: { color: C.purple, transparency: 80 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 9.5, y: 4.5, w: 6, h: 6,
    fill: { color: C.sky, transparency: 80 }, line: { color: C.sky, transparency: 80 },
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.9, y: 0.9, w: 2.2, h: 0.45,
    fill: { color: C.bg2 }, line: { color: C.border, width: 0.75 }, rectRadius: 0.22,
  });
  s.addText("AI · MULTI-AGENT", {
    x: 0.9, y: 0.9, w: 2.2, h: 0.45,
    fontSize: 11, fontFace: F.head, bold: true,
    color: C.textBody, align: "center", valign: "middle", charSpacing: 4, margin: 0,
  });
  s.addText("LangGraph", {
    x: 0.9, y: 1.7, w: 12, h: 1.1,
    fontSize: 72, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Multi-Agent System", {
    x: 0.9, y: 2.7, w: 12, h: 1.1,
    fontSize: 60, fontFace: F.head, bold: true, color: C.purpleSoft, margin: 0,
  });
  s.addText(
    "A modular AI system that routes user requests to the right specialist agent — " +
    "powered by Ollama running qwen3:8b 100% locally on your machine.",
    {
      x: 0.9, y: 4.1, w: 9, h: 1.0,
      fontSize: 18, fontFace: F.body, color: C.textBody, margin: 0,
    }
  );
  const pills = [
    { label: "LangGraph", color: C.purple },
    { label: "LangChain", color: C.sky },
    { label: "Ollama", color: C.emerald },
    { label: "qwen3:8b", color: C.amber },
    { label: "Streamlit", color: C.rose },
    { label: "Python", color: C.bg3 },
  ];
  let px = 0.9;
  for (const p of pills) {
    const w = pill(s, px, 5.3, p.label, p.color);
    px += w + 0.15;
  }
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.9, y: 6.1, w: 5.5, h: 0.75,
    fill: { color: C.bg2 }, line: { color: C.border, width: 0.5 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.9, y: 6.1, w: 0.08, h: 0.75,
    fill: { color: C.purple }, line: { color: C.purple },
  });
  s.addText([
    { text: "Built by ", options: { color: C.textMuted, fontSize: 13 } },
    { text: "Daksh Vashisth", options: { color: C.text, fontSize: 14, bold: true } },
    { text: "   ·   ", options: { color: C.textMuted, fontSize: 13 } },
    { text: "github.com/Dakshvashisth3108/Langgraph_agents", options: { color: C.skySoft, fontSize: 12 } },
  ], {
    x: 1.1, y: 6.1, w: 5.3, h: 0.75, valign: "middle", fontFace: F.body, margin: 0,
  });
}

// SLIDE 2 — Problem & Solution
function slideProblemSolution(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Why a multi-agent system?", "The core idea");

  card(s, { x: 0.6, y: 1.9, w: 5.9, h: 4.7, accent: C.rose });
  s.addText("❌  One giant AI", {
    x: 0.85, y: 2.05, w: 5.5, h: 0.5,
    fontSize: 22, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("A single model tries to do everything", {
    x: 0.85, y: 2.55, w: 5.5, h: 0.35,
    fontSize: 13, fontFace: F.body, color: C.textMuted, margin: 0,
  });
  s.addText([
    { text: "Hard to specialise — one prompt for all tasks", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Difficult to debug — opaque single inference call", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "No clear separation of concerns", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Adding new behaviour means rewriting the prompt", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "No memory boundary between use-cases", options: { bullet: true, color: C.textBody } },
  ], {
    x: 0.85, y: 3.1, w: 5.5, h: 3.3,
    fontSize: 14, fontFace: F.body, color: C.textBody, paraSpaceAfter: 6, margin: 0,
  });

  card(s, { x: 6.85, y: 1.9, w: 5.9, h: 4.7, accent: C.emerald });
  s.addText("✅  A team of specialists", {
    x: 7.1, y: 2.05, w: 5.5, h: 0.5,
    fontSize: 22, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Small focused agents + a router that picks the right one", {
    x: 7.1, y: 2.55, w: 5.5, h: 0.35,
    fontSize: 13, fontFace: F.body, color: C.textMuted, margin: 0,
  });
  s.addText([
    { text: "Each agent has its own prompt, temperature, behaviour", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Easy to test in isolation — pure functions", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Easy to extend — drop in a new agent + register it", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Router intelligently classifies intent with confidence", options: { bullet: true, breakLine: true, color: C.textBody } },
    { text: "Shared memory threads through the whole graph", options: { bullet: true, color: C.textBody } },
  ], {
    x: 7.1, y: 3.1, w: 5.5, h: 3.3,
    fontSize: 14, fontFace: F.body, color: C.textBody, paraSpaceAfter: 6, margin: 0,
  });

  addFooter(s, idx, total);
}

// SLIDE 3 — Tech Stack
function slideTechStack(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Tech stack — what each piece does", "Tools & frameworks");

  const items = [
    { icon: "🧠", title: "qwen3:8b", role: "Open-source 8B LLM — runs locally", color: C.purple },
    { icon: "🦙", title: "Ollama", role: "Local LLM runtime (port 11434)", color: C.emerald },
    { icon: "🔗", title: "LangChain", role: "LLM abstraction & message types", color: C.sky },
    { icon: "🕸️", title: "LangGraph", role: "Multi-agent orchestration graph", color: C.purpleSoft },
    { icon: "🎨", title: "Streamlit", role: "Modern Python web chat UI", color: C.rose },
    { icon: "🐍", title: "Python 3.10+", role: "Glue, agents, state, utils", color: C.amber },
    { icon: "📦", title: "python-dotenv", role: "Loads .env config at runtime", color: C.bg3 },
    { icon: "📝", title: "Text prompts", role: "Editable .txt templates", color: C.skySoft },
  ];

  const cols = 4;
  const cardW = 2.95;
  const cardH = 2.1;
  const gapX = 0.25;
  const gapY = 0.3;
  const startX = 0.6;
  const startY = 1.95;

  items.forEach((item, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    card(s, { x, y, w: cardW, h: cardH, accent: item.color });
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.25, y: y + 0.25, w: 0.7, h: 0.7,
      fill: { color: item.color }, line: { color: item.color },
    });
    s.addText(item.icon, {
      x: x + 0.25, y: y + 0.25, w: 0.7, h: 0.7,
      fontSize: 24, align: "center", valign: "middle", margin: 0,
    });
    s.addText(item.title, {
      x: x + 0.25, y: y + 1.05, w: cardW - 0.5, h: 0.4,
      fontSize: 17, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText(item.role, {
      x: x + 0.25, y: y + 1.45, w: cardW - 0.5, h: 0.55,
      fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });

  addFooter(s, idx, total);
}

// SLIDE 4 — Architecture
function slideArchitecture(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Architecture — the flow at a glance", "How agents connect");

  const userX = 5.5, userY = 1.85, boxW = 2.3, boxH = 0.75;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: userX, y: userY, w: boxW, h: boxH,
    fill: { color: C.bg2 }, line: { color: C.border, width: 1 }, rectRadius: 0.12,
  });
  s.addText("👤  USER", {
    x: userX, y: userY, w: boxW, h: boxH,
    fontSize: 16, fontFace: F.head, bold: true, color: C.text,
    align: "center", valign: "middle", margin: 0,
  });
  s.addShape(pres.shapes.LINE, {
    x: userX + boxW / 2, y: userY + boxH, w: 0, h: 0.5,
    line: { color: C.textMuted, width: 2, endArrowType: "triangle" },
  });

  const routerX = 4.5, routerY = 3.15, routerW = 4.3, routerH = 1.0;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: routerX, y: routerY, w: routerW, h: routerH,
    fill: { color: C.purple }, line: { color: C.purple, width: 0 }, rectRadius: 0.14,
  });
  s.addText([
    { text: "🚦  ROUTER AGENT", options: { fontSize: 17, bold: true, color: C.white, breakLine: true } },
    { text: "qwen3:8b classifies intent (with confidence gate)", options: { fontSize: 11, color: C.text } },
  ], {
    x: routerX, y: routerY, w: routerW, h: routerH,
    fontFace: F.head, align: "center", valign: "middle", margin: 0,
  });

  s.addShape(pres.shapes.OVAL, {
    x: 6.4, y: 4.4, w: 0.5, h: 0.5,
    fill: { color: C.bg2 }, line: { color: C.amber, width: 1.5 },
  });
  s.addText("?", {
    x: 6.4, y: 4.4, w: 0.5, h: 0.5,
    fontSize: 18, fontFace: F.head, bold: true, color: C.amber,
    align: "center", valign: "middle", margin: 0,
  });

  s.addShape(pres.shapes.LINE, {
    x: 6.6, y: 4.9, w: -3.6, h: 0.5,
    line: { color: C.purpleSoft, width: 2, endArrowType: "triangle" },
  });
  s.addShape(pres.shapes.LINE, {
    x: 6.7, y: 4.9, w: 3.6, h: 0.5,
    line: { color: C.skySoft, width: 2, endArrowType: "triangle" },
  });
  s.addText("movie_agent", {
    x: 4.0, y: 4.95, w: 1.6, h: 0.3,
    fontSize: 10, fontFace: F.mono, color: C.purpleSoft, align: "center", margin: 0,
  });
  s.addText("story_agent", {
    x: 7.7, y: 4.95, w: 1.6, h: 0.3,
    fontSize: 10, fontFace: F.mono, color: C.skySoft, align: "center", margin: 0,
  });

  const maX = 1.7, maY = 5.4, maW = 3.6, maH = 1.0;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: maX, y: maY, w: maW, h: maH,
    fill: { color: C.bg2 }, line: { color: C.purple, width: 1.5 }, rectRadius: 0.14,
  });
  s.addText([
    { text: "🎬  MOVIE AGENT", options: { fontSize: 16, bold: true, color: C.purpleSoft, breakLine: true } },
    { text: "Explains plots, spoiler-light", options: { fontSize: 10, color: C.textBody } },
  ], {
    x: maX, y: maY, w: maW, h: maH,
    fontFace: F.head, align: "center", valign: "middle", margin: 0,
  });

  const saX = 8.0, saY = 5.4, saW = 3.6, saH = 1.0;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: saX, y: saY, w: saW, h: saH,
    fill: { color: C.bg2 }, line: { color: C.sky, width: 1.5 }, rectRadius: 0.14,
  });
  s.addText([
    { text: "📖  STORY AGENT", options: { fontSize: 16, bold: true, color: C.skySoft, breakLine: true } },
    { text: "Writes short creative stories", options: { fontSize: 10, color: C.textBody } },
  ], {
    x: saX, y: saY, w: saW, h: saH,
    fontFace: F.head, align: "center", valign: "middle", margin: 0,
  });

  card(s, { x: 11.0, y: 1.85, w: 1.85, h: 1.7, accent: C.emerald });
  s.addText("State", {
    x: 11.15, y: 1.95, w: 1.6, h: 0.3,
    fontSize: 12, fontFace: F.head, bold: true, color: C.emerald, margin: 0,
  });
  s.addText([
    { text: "user_input", options: { breakLine: true, fontSize: 9, color: C.textBody, fontFace: F.mono } },
    { text: "selected_agent", options: { breakLine: true, fontSize: 9, color: C.textBody, fontFace: F.mono } },
    { text: "response", options: { breakLine: true, fontSize: 9, color: C.textBody, fontFace: F.mono } },
    { text: "history", options: { fontSize: 9, color: C.textBody, fontFace: F.mono } },
  ], {
    x: 11.15, y: 2.3, w: 1.6, h: 1.15, paraSpaceAfter: 2, margin: 0,
  });

  s.addText("➜  State flows top-down through nodes; conditional edge picks the branch.", {
    x: 0.6, y: 6.6, w: 12.1, h: 0.3,
    fontSize: 11, fontFace: F.body, italic: true, color: C.textMuted,
    align: "center", margin: 0,
  });
  addFooter(s, idx, total);
}

// SLIDE 5 — Folder Structure
function slideFolderStructure(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Folder structure — one job per folder", "Code organization");

  card(s, { x: 0.6, y: 1.95, w: 6.1, h: 4.95, accent: C.purple });
  const tree = [
    "multi_agent_system/",
    "├── agents/             # specialist team",
    "│   ├── _base.py        # shared run_agent() pipeline",
    "│   ├── movie_agent.py  # 🎬 movie expert",
    "│   ├── story_agent.py  # 📖 storyteller",
    "│   └── router_agent.py # 🚦 LLM-based router",
    "│",
    "├── graph/",
    "│   └── workflow.py     # LangGraph state machine",
    "│",
    "├── prompts/            # plain-text templates",
    "│   ├── movie_prompt.txt",
    "│   └── story_prompt.txt",
    "│",
    "├── utils/",
    "│   ├── llm.py          # one ChatOllama factory",
    "│   ├── memory.py       # windowed message buffer",
    "│   └── logging_setup.py",
    "│",
    "├── frontend/app.py     # Streamlit chat UI",
    "├── main.py             # terminal chatbot",
    "├── requirements.txt",
    "├── .env",
    "└── README.md",
  ];
  s.addText(tree.map((line, i) => ({
    text: line,
    options: { breakLine: i < tree.length - 1, color: C.textBody, fontSize: 11, fontFace: F.mono },
  })), {
    x: 0.85, y: 2.1, w: 5.7, h: 4.7, margin: 0,
  });

  const principles = [
    { icon: "🎯", title: "One folder, one job", body: "Agents, graph, prompts, utils, frontend each own a single responsibility." },
    { icon: "📂", title: "Prompts as .txt files", body: "Non-developers can tune model behaviour without touching Python." },
    { icon: "🔌", title: "Single LLM loader", body: "utils/llm.py is the only place that knows about Ollama. Swap providers in one file." },
    { icon: "🧬", title: "Shared agent base", body: "_base.run_agent() captures load-prompt → call-LLM → handle-errors once." },
  ];
  principles.forEach((p, i) => {
    const y = 1.95 + i * 1.27;
    card(s, { x: 6.95, y, w: 5.75, h: 1.13, accent: C.sky });
    s.addText(p.icon, {
      x: 7.1, y, w: 0.6, h: 1.13,
      fontSize: 26, align: "center", valign: "middle", margin: 0,
    });
    s.addText(p.title, {
      x: 7.75, y: y + 0.15, w: 4.85, h: 0.4,
      fontSize: 15, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText(p.body, {
      x: 7.75, y: y + 0.5, w: 4.85, h: 0.6,
      fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 6 — Router
function slideRouter(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Router agent — intelligent intent classification", "🚦  routing");

  const steps = [
    {
      n: "1", title: "LLM classification", color: C.purple,
      body: "qwen3:8b reads the user message + recent history and emits JSON:",
      code: "{ \"agent\": \"movie_agent\", \"confidence\": 0.95, \"reason\": \"…\" }",
    },
    {
      n: "2", title: "Confidence gate", color: C.amber,
      body: "If confidence ≥ 0.60 → trust the LLM's pick.\nIf below → default to story_agent (safer fallback).",
    },
    {
      n: "3", title: "Keyword safety net", color: C.emerald,
      body: "If the LLM is unreachable or its output is unparseable, fall back to a simple keyword match on movie / film / plot / cinema / story of.",
    },
  ];
  steps.forEach((stp, i) => {
    const y = 1.95 + i * 1.62;
    card(s, { x: 0.6, y, w: 7.5, h: 1.48, accent: stp.color });
    s.addShape(pres.shapes.OVAL, {
      x: 0.85, y: y + 0.27, w: 0.85, h: 0.85,
      fill: { color: stp.color }, line: { color: stp.color },
    });
    s.addText(stp.n, {
      x: 0.85, y: y + 0.27, w: 0.85, h: 0.85,
      fontSize: 32, fontFace: F.head, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(stp.title, {
      x: 1.95, y: y + 0.18, w: 5.4, h: 0.4,
      fontSize: 17, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    if (stp.code) {
      s.addText(stp.body, {
        x: 1.95, y: y + 0.55, w: 5.4, h: 0.35,
        fontSize: 12, fontFace: F.body, color: C.textBody, margin: 0,
      });
      s.addText(stp.code, {
        x: 1.95, y: y + 0.92, w: 5.4, h: 0.4,
        fontSize: 11, fontFace: F.mono, color: C.skySoft, margin: 0,
      });
    } else {
      s.addText(stp.body, {
        x: 1.95, y: y + 0.55, w: 5.4, h: 0.85,
        fontSize: 12, fontFace: F.body, color: C.textBody, margin: 0,
      });
    }
  });

  card(s, { x: 8.35, y: 1.95, w: 4.4, h: 4.85, accent: C.rose });
  s.addText("Why LLM-driven?", {
    x: 8.6, y: 2.1, w: 4.0, h: 0.4,
    fontSize: 17, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Pure keywords can't handle follow-ups.", {
    x: 8.6, y: 2.5, w: 4.0, h: 0.3,
    fontSize: 11, fontFace: F.body, italic: true, color: C.textMuted, margin: 0,
  });
  s.addText("User says:", {
    x: 8.6, y: 3.0, w: 4.0, h: 0.3,
    fontSize: 11, fontFace: F.head, bold: true, color: C.textMuted, margin: 0,
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 8.6, y: 3.3, w: 4.0, h: 0.7,
    fill: { color: C.bg3 }, line: { color: C.border }, rectRadius: 0.1,
  });
  s.addText("\"What else has that director made?\"", {
    x: 8.7, y: 3.3, w: 3.8, h: 0.7,
    fontSize: 12, fontFace: F.body, italic: true, color: C.text,
    valign: "middle", margin: 0,
  });
  s.addText("No movie keyword — but the LLM sees the prior turn was about Inception and confidently routes to MovieAgent.", {
    x: 8.6, y: 4.15, w: 4.0, h: 1.4,
    fontSize: 12, fontFace: F.body, color: C.textBody, margin: 0,
  });
  s.addText("✓  History-aware\n✓  Confidence-gated\n✓  Resilient to LLM downtime", {
    x: 8.6, y: 5.55, w: 4.0, h: 1.2,
    fontSize: 13, fontFace: F.body, color: C.emerald, margin: 0, paraSpaceAfter: 4,
  });
  addFooter(s, idx, total);
}

// SLIDE 7 — Specialists
function slideSpecialists(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Specialist agents — small, focused, swappable", "🎭  the workers");

  card(s, { x: 0.6, y: 1.95, w: 6.05, h: 4.8, accent: C.purple });
  s.addShape(pres.shapes.OVAL, {
    x: 0.9, y: 2.15, w: 0.8, h: 0.8,
    fill: { color: C.purple }, line: { color: C.purple },
  });
  s.addText("🎬", { x: 0.9, y: 2.15, w: 0.8, h: 0.8, fontSize: 28, align: "center", valign: "middle", margin: 0 });
  s.addText("MovieAgent", {
    x: 1.85, y: 2.2, w: 4.5, h: 0.5,
    fontSize: 22, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Spoiler-light film expert", {
    x: 1.85, y: 2.65, w: 4.5, h: 0.3,
    fontSize: 12, fontFace: F.body, color: C.textMuted, margin: 0,
  });
  const movieRows = [
    ["temperature", "0.5"],
    ["max_tokens", "1024"],
    ["prompt file", "movie_prompt.txt"],
    ["behaviour", "explain plots in <120 words, avoid major spoilers"],
  ];
  movieRows.forEach((row, i) => {
    const y = 3.15 + i * 0.65;
    s.addText(row[0], {
      x: 0.9, y, w: 1.6, h: 0.5,
      fontSize: 11, fontFace: F.mono, color: C.purpleSoft, valign: "middle", margin: 0,
    });
    s.addText(row[1], {
      x: 2.55, y, w: 3.8, h: 0.5,
      fontSize: 12, fontFace: F.body, color: C.textBody, valign: "middle", margin: 0,
    });
  });

  card(s, { x: 6.95, y: 1.95, w: 6.05, h: 4.8, accent: C.sky });
  s.addShape(pres.shapes.OVAL, {
    x: 7.25, y: 2.15, w: 0.8, h: 0.8,
    fill: { color: C.sky }, line: { color: C.sky },
  });
  s.addText("📖", { x: 7.25, y: 2.15, w: 0.8, h: 0.8, fontSize: 28, align: "center", valign: "middle", margin: 0 });
  s.addText("StoryAgent", {
    x: 8.2, y: 2.2, w: 4.5, h: 0.5,
    fontSize: 22, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Creative short-story writer", {
    x: 8.2, y: 2.65, w: 4.5, h: 0.3,
    fontSize: 12, fontFace: F.body, color: C.textMuted, margin: 0,
  });
  const storyRows = [
    ["temperature", "0.9"],
    ["max_tokens", "1500"],
    ["prompt file", "story_prompt.txt"],
    ["behaviour", "200–300 word stories with beginning, middle, end"],
  ];
  storyRows.forEach((row, i) => {
    const y = 3.15 + i * 0.65;
    s.addText(row[0], {
      x: 7.25, y, w: 1.6, h: 0.5,
      fontSize: 11, fontFace: F.mono, color: C.skySoft, valign: "middle", margin: 0,
    });
    s.addText(row[1], {
      x: 8.9, y, w: 3.8, h: 0.5,
      fontSize: 12, fontFace: F.body, color: C.textBody, valign: "middle", margin: 0,
    });
  });

  addFooter(s, idx, total);
}

// SLIDE 8 — LangGraph
function slideLangGraph(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "LangGraph orchestration — the state machine", "🕸️  the wiring");

  card(s, { x: 0.6, y: 1.95, w: 7.3, h: 4.85, accent: C.purple, fill: "0B1220" });
  s.addText("graph/workflow.py", {
    x: 0.85, y: 2.05, w: 6.8, h: 0.3,
    fontSize: 11, fontFace: F.mono, color: C.textMuted, margin: 0,
  });
  const code = [
    "from langgraph.graph import StateGraph, START, END",
    "",
    "class GraphState(TypedDict, total=False):",
    "    user_input: str",
    "    selected_agent: str",
    "    response: str",
    "    history: list[BaseMessage]",
    "",
    "graph = StateGraph(GraphState)",
    "graph.add_node(\"router_agent\", router_agent)",
    "graph.add_node(\"movie_agent\",  movie_agent)",
    "graph.add_node(\"story_agent\",  story_agent)",
    "",
    "graph.add_edge(START, \"router_agent\")",
    "graph.add_conditional_edges(",
    "    \"router_agent\", _route_decision,",
    "    { \"movie_agent\": \"movie_agent\",",
    "      \"story_agent\": \"story_agent\" },",
    ")",
    "graph.add_edge(\"movie_agent\", END)",
    "graph.add_edge(\"story_agent\", END)",
    "",
    "workflow = graph.compile()",
  ];
  s.addText(code.map((l, i) => ({
    text: l, options: { breakLine: i < code.length - 1, fontSize: 11.5, fontFace: F.mono, color: C.textBody },
  })), {
    x: 0.85, y: 2.4, w: 6.8, h: 4.35, margin: 0,
  });

  const concepts = [
    { icon: "📦", title: "Nodes", body: "Plain Python functions: state in → state out." },
    { icon: "➡️", title: "Edges", body: "Directed arrows: START → router → specialist → END." },
    { icon: "❓", title: "Conditional edges", body: "Read a state field to dynamically pick the next node." },
    { icon: "🧊", title: "State (TypedDict)", body: "Shared, typed dictionary flowing through every node." },
  ];
  concepts.forEach((c, i) => {
    const y = 1.95 + i * 1.235;
    card(s, { x: 8.15, y, w: 4.6, h: 1.1, accent: C.sky });
    s.addText(c.icon, {
      x: 8.3, y, w: 0.6, h: 1.1, fontSize: 22,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(c.title, {
      x: 8.95, y: y + 0.15, w: 3.7, h: 0.35,
      fontSize: 14, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText(c.body, {
      x: 8.95, y: y + 0.5, w: 3.7, h: 0.6,
      fontSize: 10.5, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 9 — Memory
function slideMemory(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Memory — letting follow-ups make sense", "🧠  short-term context");

  const steps = [
    { t: "User types", color: C.purple, icon: "👤" },
    { t: "memory.get_messages()", color: C.sky, icon: "📚" },
    { t: "workflow.invoke()\nwith history", color: C.emerald, icon: "🕸️" },
    { t: "Agent injects history\ninto prompt", color: C.amber, icon: "🤖" },
    { t: "memory.add()", color: C.purpleSoft, icon: "💾" },
  ];
  const boxW = 2.25, boxH = 1.7, gap = 0.2, startX = 0.6, baseY = 1.95;
  steps.forEach((stp, i) => {
    const x = startX + i * (boxW + gap);
    card(s, { x, y: baseY, w: boxW, h: boxH, accent: stp.color });
    s.addShape(pres.shapes.OVAL, {
      x: x + (boxW - 0.7) / 2, y: baseY + 0.2, w: 0.7, h: 0.7,
      fill: { color: stp.color }, line: { color: stp.color },
    });
    s.addText(stp.icon, {
      x: x + (boxW - 0.7) / 2, y: baseY + 0.2, w: 0.7, h: 0.7,
      fontSize: 24, align: "center", valign: "middle", margin: 0,
    });
    s.addText(stp.t, {
      x: x + 0.1, y: baseY + 0.95, w: boxW - 0.2, h: 0.7,
      fontSize: 11, fontFace: F.body, color: C.textBody,
      align: "center", valign: "top", margin: 0,
    });
    if (i < steps.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: x + boxW, y: baseY + boxH / 2, w: gap, h: 0,
        line: { color: C.textMuted, width: 1.5, endArrowType: "triangle" },
      });
    }
  });

  card(s, { x: 0.6, y: 4.0, w: 6.5, h: 2.85, accent: C.sky });
  s.addText("ConversationMemory  ·  utils/memory.py", {
    x: 0.85, y: 4.15, w: 6.0, h: 0.35,
    fontSize: 13, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("A windowed buffer of LangChain HumanMessage / AIMessage objects, auto-trimmed via trim_messages() to the last 10 messages.", {
    x: 0.85, y: 4.5, w: 6.0, h: 0.7,
    fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
  });
  s.addText([
    { text: "add_user_message(content)", options: { breakLine: true, fontFace: F.mono, color: C.skySoft, fontSize: 11 } },
    { text: "add_assistant_message(content)", options: { breakLine: true, fontFace: F.mono, color: C.skySoft, fontSize: 11 } },
    { text: "get_messages()  →  list[BaseMessage]", options: { breakLine: true, fontFace: F.mono, color: C.skySoft, fontSize: 11 } },
    { text: "clear()", options: { fontFace: F.mono, color: C.skySoft, fontSize: 11 } },
  ], {
    x: 0.85, y: 5.3, w: 6.0, h: 1.45, paraSpaceAfter: 3, margin: 0,
  });

  card(s, { x: 7.35, y: 4.0, w: 5.4, h: 2.85, accent: C.emerald });
  s.addText("Why this matters", {
    x: 7.6, y: 4.15, w: 5.0, h: 0.35,
    fontSize: 13, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText([
    { text: "Without memory:", options: { color: C.textMuted, fontSize: 11, breakLine: true } },
    { text: "\"What else has that director made?\" → confused.", options: { color: C.rose, italic: true, fontSize: 11.5, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "With memory:", options: { color: C.textMuted, fontSize: 11, breakLine: true } },
    { text: "The LLM sees the prior turn was about Inception →  answers about Christopher Nolan correctly.", options: { color: C.emerald, italic: true, fontSize: 11.5 } },
  ], {
    x: 7.6, y: 4.5, w: 5.0, h: 2.25, paraSpaceAfter: 2, margin: 0,
  });
  addFooter(s, idx, total);
}

// SLIDE 10 — Request Flow
function slideRequestFlow(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Request flow — one query, step by step", "🔁  end-to-end trace");

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.6, y: 1.95, w: 12.15, h: 0.55,
    fill: { color: C.bg2 }, line: { color: C.purple, width: 1 }, rectRadius: 0.12,
  });
  s.addText([
    { text: "User input:  ", options: { fontFace: F.head, bold: true, color: C.textMuted, fontSize: 12 } },
    { text: "\"Tell me the plot of Inception\"", options: { fontFace: F.body, italic: true, color: C.text, fontSize: 13 } },
  ], {
    x: 0.85, y: 1.95, w: 11.7, h: 0.55, valign: "middle", margin: 0,
  });

  const flow = [
    { n: "1", title: "Streamlit catches input", body: "frontend/app.py calls workflow.invoke({user_input, history})", color: C.purple },
    { n: "2", title: "Graph enters router_agent", body: "LangGraph passes the state into the router node", color: C.sky },
    { n: "3", title: "Router classifies with qwen3:8b", body: "JSON: { agent: 'movie_agent', confidence: 0.95 }  →  passes confidence gate", color: C.amber },
    { n: "4", title: "Conditional edge dispatches", body: "_route_decision reads state['selected_agent'] = 'movie_agent'  →  routes there", color: C.emerald },
    { n: "5", title: "MovieAgent runs _base.run_agent()", body: "Loads movie_prompt.txt, injects history, calls Ollama, strips <think> blocks", color: C.purpleSoft },
    { n: "6", title: "Response returns + memory updates", body: "UI shows 🎬 badge + reply; memory appends both messages for the next turn", color: C.skySoft },
  ];

  flow.forEach((f, i) => {
    const y = 2.7 + i * 0.7;
    s.addShape(pres.shapes.OVAL, {
      x: 0.6, y, w: 0.55, h: 0.55,
      fill: { color: f.color }, line: { color: f.color },
    });
    s.addText(f.n, {
      x: 0.6, y, w: 0.55, h: 0.55,
      fontSize: 18, fontFace: F.head, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(f.title, {
      x: 1.3, y: y - 0.02, w: 4.2, h: 0.3,
      fontSize: 13, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText(f.body, {
      x: 1.3, y: y + 0.28, w: 11.4, h: 0.4,
      fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 11 — Implementation
function slideImplementation(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Implementation — the shared agent pipeline", "🧬  agents/_base.py");

  const stages = [
    { icon: "✋", title: "Validate input", body: "Reject blank queries early — save a model call.", color: C.amber },
    { icon: "📄", title: "Load prompt", body: "Read prompts/<name>.txt  ·  raise FileNotFoundError if missing.", color: C.purple },
    { icon: "🧷", title: "Render template", body: "Fill {history} and {user_input} placeholders with real data.", color: C.sky },
    { icon: "🤖", title: "Call LLM", body: "get_llm(temperature, max_tokens) → ChatOllama → qwen3:8b.", color: C.emerald },
    { icon: "🧹", title: "Clean output", body: "Strip <think>…</think> reasoning blocks before returning text.", color: C.purpleSoft },
  ];
  stages.forEach((st, i) => {
    const y = 1.95 + i * 0.98;
    card(s, { x: 0.6, y, w: 7.3, h: 0.85, accent: st.color });
    s.addShape(pres.shapes.OVAL, {
      x: 0.85, y: y + 0.15, w: 0.55, h: 0.55,
      fill: { color: st.color }, line: { color: st.color },
    });
    s.addText(st.icon, {
      x: 0.85, y: y + 0.15, w: 0.55, h: 0.55,
      fontSize: 20, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.title, {
      x: 1.55, y: y + 0.1, w: 5.6, h: 0.3,
      fontSize: 14, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText(st.body, {
      x: 1.55, y: y + 0.4, w: 6.2, h: 0.4,
      fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });

  card(s, { x: 8.15, y: 1.95, w: 4.6, h: 4.85, accent: C.emerald, fill: "0B1220" });
  s.addText("agents/movie_agent.py", {
    x: 8.35, y: 2.05, w: 4.2, h: 0.3,
    fontSize: 11, fontFace: F.mono, color: C.textMuted, margin: 0,
  });
  const py = [
    "def get_movie_response(",
    "    user_input: str,",
    "    history=None,",
    ") -> str:",
    "    return run_agent(",
    "      agent_name=\"movie_agent\",",
    "      prompt_file=\"movie_prompt.txt\",",
    "      user_input=user_input,",
    "      history=history,",
    "      temperature=0.5,",
    "      max_tokens=1024,",
    "    )",
  ];
  s.addText(py.map((l, i) => ({
    text: l, options: { breakLine: i < py.length - 1, fontSize: 11, fontFace: F.mono, color: C.textBody },
  })), {
    x: 8.35, y: 2.4, w: 4.2, h: 3.5, margin: 0,
  });
  s.addText("➜  Adding a new agent = ~25 lines.", {
    x: 8.35, y: 6.05, w: 4.2, h: 0.6,
    fontSize: 12, fontFace: F.body, italic: true, color: C.emerald, margin: 0,
  });
  addFooter(s, idx, total);
}

// SLIDE 12 — Complexity
function slideComplexity(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Complexity — what it costs to run", "📊  performance");

  const stats = [
    { value: "≤ 2", label: "LLM calls per turn", note: "(1 router + 1 specialist)", color: C.purple },
    { value: "O(1)", label: "Memory growth per turn", note: "auto-trimmed to last 10 msgs", color: C.sky },
    { value: "~ 5 GB", label: "RAM for qwen3:8b", note: "Q4_K_M quantized weights", color: C.emerald },
    { value: "0", label: "External API cost", note: "everything runs locally", color: C.amber },
  ];
  stats.forEach((st, i) => {
    const x = 0.6 + i * 3.075;
    card(s, { x, y: 1.95, w: 2.9, h: 1.85, accent: st.color });
    s.addText(st.value, {
      x: x + 0.1, y: 2.05, w: 2.7, h: 0.85,
      fontSize: 36, fontFace: F.head, bold: true, color: st.color,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: x + 0.1, y: 2.95, w: 2.7, h: 0.35,
      fontSize: 12, fontFace: F.head, bold: true, color: C.text,
      align: "center", margin: 0,
    });
    s.addText(st.note, {
      x: x + 0.1, y: 3.3, w: 2.7, h: 0.4,
      fontSize: 10, fontFace: F.body, italic: true, color: C.textMuted,
      align: "center", margin: 0,
    });
  });

  card(s, { x: 0.6, y: 4.05, w: 12.15, h: 2.85, accent: C.sky });
  s.addText("Per-turn breakdown", {
    x: 0.85, y: 4.2, w: 11.7, h: 0.4,
    fontSize: 15, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  const headers = ["Phase", "Time", "Tokens", "Notes"];
  const rows = [
    ["Router LLM classification", "≈ 0.3 – 1 s", "~ 200 in / ~ 60 out", "temp=0.0, deterministic"],
    ["Specialist LLM (movie)", "≈ 2 – 5 s", "~ 400 in / ~ 250 out", "temp=0.5, factual"],
    ["Specialist LLM (story)", "≈ 4 – 8 s", "~ 400 in / ~ 600 out", "temp=0.9, creative"],
    ["Graph overhead", "< 50 ms", "—", "pure Python, in-process"],
    ["Total per query", "≈ 2 – 10 s", "—", "dominated by model inference"],
  ];
  const colX = [0.85, 4.55, 6.85, 9.0];
  const colW = [3.6, 2.2, 2.0, 3.65];
  headers.forEach((h, i) => {
    s.addText(h, {
      x: colX[i], y: 4.65, w: colW[i], h: 0.3,
      fontSize: 11, fontFace: F.head, bold: true, color: C.textMuted,
      charSpacing: 3, margin: 0,
    });
  });
  rows.forEach((row, ri) => {
    const y = 4.95 + ri * 0.38;
    row.forEach((cell, ci) => {
      s.addText(cell, {
        x: colX[ci], y, w: colW[ci], h: 0.35,
        fontSize: 11, fontFace: ci === 1 || ci === 2 ? F.mono : F.body,
        color: ri === rows.length - 1 ? C.emerald : C.textBody,
        bold: ri === rows.length - 1, margin: 0,
      });
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 13 — Reliability
function slideReliability(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Reliability — failure modes & safety nets", "🛡️  resilience");

  const fails = [
    {
      title: "Ollama is down", icon: "🔌", color: C.rose,
      what: "Health check fails on /  (port 11434)",
      how: "OllamaConnectionError caught everywhere → user sees: \"Please run `ollama serve` and `ollama pull qwen3:8b`.\"",
    },
    {
      title: "Prompt file missing", icon: "📄", color: C.amber,
      what: "load_prompt() can't find prompts/<name>.txt",
      how: "FileNotFoundError → friendly inline error in the chat bubble (not a crash).",
    },
    {
      title: "Router output unparseable", icon: "🚦", color: C.purple,
      what: "qwen3:8b returns invalid JSON or unknown agent label",
      how: "Falls back to keyword matching → still resolves to a valid agent.",
    },
    {
      title: "qwen3 leaks reasoning", icon: "🧠", color: C.sky,
      what: "<think>...</think> blocks appear in the response",
      how: "_strip_thinking() regex removes them before the text reaches the UI.",
    },
    {
      title: "Empty / blank input", icon: "✋", color: C.emerald,
      what: "User submits an empty message",
      how: "Each agent returns a polite \"please share something\" — zero model cost.",
    },
    {
      title: "Unknown exception", icon: "💥", color: C.purpleSoft,
      what: "Anything else goes wrong",
      how: "Catch-all logs full traceback → UI shows \"⚠️ Something went wrong\" → app stays alive.",
    },
  ];

  const cols = 3;
  const cardW = 4.05;
  const cardH = 2.4;
  fails.forEach((f, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = 0.6 + col * (cardW + 0.1);
    const y = 1.95 + row * (cardH + 0.15);
    card(s, { x, y, w: cardW, h: cardH, accent: f.color });
    s.addText(f.icon, {
      x: x + 0.2, y: y + 0.15, w: 0.6, h: 0.6, fontSize: 26,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(f.title, {
      x: x + 0.85, y: y + 0.18, w: cardW - 1.0, h: 0.4,
      fontSize: 14, fontFace: F.head, bold: true, color: C.text, margin: 0,
    });
    s.addText("WHAT", {
      x: x + 0.2, y: y + 0.85, w: cardW - 0.4, h: 0.25,
      fontSize: 9, fontFace: F.head, bold: true, color: C.textMuted,
      charSpacing: 3, margin: 0,
    });
    s.addText(f.what, {
      x: x + 0.2, y: y + 1.05, w: cardW - 0.4, h: 0.4,
      fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
    });
    s.addText("HOW WE HANDLE IT", {
      x: x + 0.2, y: y + 1.5, w: cardW - 0.4, h: 0.25,
      fontSize: 9, fontFace: F.head, bold: true, color: C.textMuted,
      charSpacing: 3, margin: 0,
    });
    s.addText(f.how, {
      x: x + 0.2, y: y + 1.7, w: cardW - 0.4, h: 0.65,
      fontSize: 10.5, fontFace: F.body, color: C.textBody, margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 14 — Frontend
function slideFrontend(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Frontend — modern Streamlit chat", "🎨  the user-facing skin");

  const browserX = 0.6, browserY = 1.95, browserW = 8.3, browserH = 4.95;
  s.addShape(pres.shapes.RECTANGLE, {
    x: browserX, y: browserY, w: browserW, h: browserH,
    fill: { color: "020617" }, line: { color: C.border, width: 1 },
    shadow: { type: "outer", color: "000000", blur: 8, offset: 3, angle: 135, opacity: 0.4 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: browserX, y: browserY, w: browserW, h: 0.42,
    fill: { color: C.bg3 }, line: { color: C.bg3 },
  });
  ["F43F5E", "F59E0B", "10B981"].forEach((col, i) => {
    s.addShape(pres.shapes.OVAL, {
      x: browserX + 0.12 + i * 0.22, y: browserY + 0.12, w: 0.18, h: 0.18,
      fill: { color: col }, line: { color: col },
    });
  });
  s.addText("localhost:8501  ·  LangGraph Multi-Agent System", {
    x: browserX + 0.85, y: browserY + 0.05, w: browserW - 1.0, h: 0.32,
    fontSize: 10, fontFace: F.body, color: C.textMuted, valign: "middle", margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: browserX + 0.05, y: browserY + 0.45, w: 1.9, h: browserH - 0.5,
    fill: { color: C.bg2 }, line: { color: C.bg2 },
  });
  s.addText("⚙️  System Info", {
    x: browserX + 0.15, y: browserY + 0.55, w: 1.7, h: 0.3,
    fontSize: 10, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText([
    { text: "Model", options: { breakLine: true, fontSize: 8, color: C.textMuted } },
    { text: "qwen3:8b", options: { breakLine: true, fontSize: 9, color: C.text, fontFace: F.mono } },
    { text: " ", options: { breakLine: true } },
    { text: "Framework", options: { breakLine: true, fontSize: 8, color: C.textMuted } },
    { text: "LangGraph", options: { breakLine: true, fontSize: 9, color: C.text, fontFace: F.mono } },
    { text: " ", options: { breakLine: true } },
    { text: "Backend", options: { breakLine: true, fontSize: 8, color: C.textMuted } },
    { text: "Ollama", options: { fontSize: 9, color: C.text, fontFace: F.mono } },
  ], {
    x: browserX + 0.15, y: browserY + 0.95, w: 1.7, h: 1.8, paraSpaceAfter: 1, margin: 0,
  });

  s.addShape(pres.shapes.OVAL, {
    x: browserX + 2.1, y: browserY + 0.55, w: 0.3, h: 0.3,
    fill: { color: C.bg3 }, line: { color: C.bg3 },
  });
  s.addText("🧑  14:32", {
    x: browserX + 2.5, y: browserY + 0.55, w: 4, h: 0.3,
    fontSize: 9, fontFace: F.body, color: C.textMuted, valign: "middle", margin: 0,
  });
  s.addText("Tell me the plot of Inception", {
    x: browserX + 2.5, y: browserY + 0.85, w: 5.6, h: 0.3,
    fontSize: 12, fontFace: F.body, color: C.text, margin: 0,
  });

  s.addShape(pres.shapes.OVAL, {
    x: browserX + 2.1, y: browserY + 1.5, w: 0.3, h: 0.3,
    fill: { color: C.bg3 }, line: { color: C.bg3 },
  });
  pill(s, browserX + 2.5, browserY + 1.5, "🎬 MovieAgent", C.purple);
  s.addText("14:32", {
    x: browserX + 4.6, y: browserY + 1.5, w: 1, h: 0.3,
    fontSize: 9, fontFace: F.body, color: C.textMuted, valign: "middle", margin: 0,
  });
  s.addText("🎬  Inception (2010, Sci-Fi Thriller, dir. Christopher Nolan)", {
    x: browserX + 2.5, y: browserY + 1.95, w: 5.6, h: 0.3,
    fontSize: 11, fontFace: F.head, italic: true, color: C.text, margin: 0,
  });
  s.addText("A skilled thief who steals secrets from people's dreams is offered a chance to redeem his life — if he can pull off the impossible: planting an idea inside a corporate heir's mind.", {
    x: browserX + 2.5, y: browserY + 2.3, w: 5.6, h: 1.2,
    fontSize: 11, fontFace: F.body, color: C.textBody, margin: 0,
  });

  s.addShape(pres.shapes.OVAL, {
    x: browserX + 2.1, y: browserY + 3.7, w: 0.3, h: 0.3,
    fill: { color: C.bg3 }, line: { color: C.bg3 },
  });
  s.addText("🧑  14:35", {
    x: browserX + 2.5, y: browserY + 3.7, w: 4, h: 0.3,
    fontSize: 9, fontFace: F.body, color: C.textMuted, valign: "middle", margin: 0,
  });
  s.addText("a tiny dragon afraid of fire", {
    x: browserX + 2.5, y: browserY + 4.0, w: 5.6, h: 0.3,
    fontSize: 12, fontFace: F.body, color: C.text, margin: 0,
  });
  s.addShape(pres.shapes.OVAL, {
    x: browserX + 2.1, y: browserY + 4.4, w: 0.3, h: 0.3,
    fill: { color: C.bg3 }, line: { color: C.bg3 },
  });
  pill(s, browserX + 2.5, browserY + 4.4, "📖 StoryAgent", C.sky);

  card(s, { x: 9.15, y: 1.95, w: 3.6, h: 4.95, accent: C.rose });
  s.addText("UI Features", {
    x: 9.35, y: 2.1, w: 3.2, h: 0.4,
    fontSize: 16, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  const feats = [
    ["🧠", "Persistent chat history"],
    ["🎟️", "Colored agent badges"],
    ["🕒", "Timestamps per message"],
    ["⏳", "Loading spinner during inference"],
    ["📥", "Download transcript (.json)"],
    ["🧹", "One-click clear chat"],
    ["📊", "Live memory metric"],
    ["⚠️", "Friendly error messages"],
  ];
  feats.forEach((f, i) => {
    const y = 2.6 + i * 0.5;
    s.addText(f[0], {
      x: 9.35, y, w: 0.45, h: 0.4,
      fontSize: 18, align: "center", valign: "middle", margin: 0,
    });
    s.addText(f[1], {
      x: 9.85, y, w: 2.7, h: 0.4,
      fontSize: 12, fontFace: F.body, color: C.textBody, valign: "middle", margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 15 — Future Improvements
function slideFuture(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  addHeader(s, "Future improvements — where this grows", "🚀  roadmap");

  const tiers = [
    {
      title: "Easy", color: C.emerald, icon: "🌱",
      items: [
        "Add a MusicAgent (recommend songs)",
        "Add a BookAgent (reading suggestions)",
        "Add a TranslatorAgent (auto-detect language)",
        "Expose Reset / Clear via UI buttons",
      ],
    },
    {
      title: "Intermediate", color: C.amber, icon: "🛠️",
      items: [
        "Long-term memory via vector store (FAISS/Chroma)",
        "Tool use — let agents search the web or query DBs",
        "Multi-step chains — one agent's output → another's input",
        "Unit tests for each node + integration tests for the graph",
        "LangSmith tracing for observability",
      ],
    },
    {
      title: "Advanced", color: C.purple, icon: "🚀",
      items: [
        "Human-in-the-loop pauses for sensitive steps",
        "Self-correcting loops with a Critic agent",
        "REST API via FastAPI + WebSocket streaming",
        "Dockerize Ollama + the app for one-command deploy",
        "Voice in/out (Whisper + a TTS model)",
      ],
    },
  ];
  tiers.forEach((tier, i) => {
    const x = 0.6 + i * 4.1;
    card(s, { x, y: 1.95, w: 4.0, h: 4.95, accent: tier.color });
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.25, y: 2.1, w: 0.7, h: 0.7,
      fill: { color: tier.color }, line: { color: tier.color },
    });
    s.addText(tier.icon, {
      x: x + 0.25, y: 2.1, w: 0.7, h: 0.7,
      fontSize: 24, align: "center", valign: "middle", margin: 0,
    });
    s.addText(tier.title, {
      x: x + 1.05, y: 2.2, w: 2.9, h: 0.5,
      fontSize: 22, fontFace: F.head, bold: true, color: tier.color, margin: 0,
    });
    s.addText(tier.items.map((it, j) => ({
      text: it, options: {
        bullet: { code: "25CF" }, breakLine: j < tier.items.length - 1,
        fontSize: 12.5, color: C.textBody, fontFace: F.body,
      },
    })), {
      x: x + 0.3, y: 3.0, w: 3.55, h: 3.8, paraSpaceAfter: 6, margin: 0,
    });
  });
  addFooter(s, idx, total);
}

// SLIDE 16 — Recap
function slideRecap(idx, total) {
  const s = pres.addSlide();
  setDarkBg(s);
  s.addShape(pres.shapes.OVAL, {
    x: -3, y: -3, w: 8, h: 8,
    fill: { color: C.purple, transparency: 85 }, line: { color: C.purple, transparency: 85 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 9.5, y: 3.5, w: 7, h: 7,
    fill: { color: C.sky, transparency: 85 }, line: { color: C.sky, transparency: 85 },
  });
  s.addText("That's the system.", {
    x: 0.9, y: 1.5, w: 11.5, h: 1.2,
    fontSize: 56, fontFace: F.head, bold: true, color: C.text, margin: 0,
  });
  s.addText("Modular agents · Smart routing · Local-first inference", {
    x: 0.9, y: 2.6, w: 11.5, h: 0.6,
    fontSize: 22, fontFace: F.head, color: C.purpleSoft, margin: 0,
  });
  const takeaways = [
    { k: "🧩  Architecture", v: "Router → conditional edge → specialist (LangGraph state machine)" },
    { k: "🧠  Intelligence", v: "qwen3:8b classifies intent with confidence; agents reason in context via history" },
    { k: "🦾  Resilience", v: "Health checks, three-tier exception handling, keyword fallback, <think> stripping" },
    { k: "📦  Modularity", v: "Add a new agent in ~25 lines — prompt file + run_agent() configuration" },
  ];
  takeaways.forEach((t, i) => {
    const y = 3.5 + i * 0.62;
    card(s, { x: 0.9, y, w: 11.5, h: 0.55, accent: i % 2 === 0 ? C.purple : C.sky, fill: C.bg2 });
    s.addText(t.k, {
      x: 1.1, y, w: 3.0, h: 0.55,
      fontSize: 13, fontFace: F.head, bold: true, color: C.text, valign: "middle", margin: 0,
    });
    s.addText(t.v, {
      x: 4.2, y, w: 8.1, h: 0.55,
      fontSize: 12, fontFace: F.body, color: C.textBody, valign: "middle", margin: 0,
    });
  });
  s.addText("github.com/Dakshvashisth3108/Langgraph_agents", {
    x: 0.9, y: 6.55, w: 11.5, h: 0.4,
    fontSize: 14, fontFace: F.mono, color: C.skySoft, margin: 0,
  });
  s.addText("Thank you 👋", {
    x: 0.9, y: 6.95, w: 11.5, h: 0.4,
    fontSize: 14, fontFace: F.head, italic: true, color: C.textMuted, margin: 0,
  });
}

const builders = [
  slideTitle, slideProblemSolution, slideTechStack, slideArchitecture,
  slideFolderStructure, slideRouter, slideSpecialists, slideLangGraph,
  slideMemory, slideRequestFlow, slideImplementation, slideComplexity,
  slideReliability, slideFrontend, slideFuture, slideRecap,
];

builders.forEach((fn, i) => fn(i + 1, builders.length));

const out = process.env.OUT_PATH || "LangGraph_Multi_Agent_System.pptx";
pres.writeFile({ fileName: out }).then(() => {
  console.log("Wrote: " + out);
});
