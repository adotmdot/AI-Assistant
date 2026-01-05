import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from openai import OpenAI

from app.tools.kpi_tool import on_time_percentage
from app.rag.faiss_store import FaissStore
from app.rag.embeddings import embed_texts

# ===============================
# System prompt
# ===============================
SYSTEM_PROMPT = """
You are FleetOps AI Assistant.

Rules:
- Use KPI data ONLY for metric questions.
- Use RAG documents for definitions, SOPs, and policy.
- Never invent numbers.
- Be concise, factual, and operational.
"""

# ===============================
# Build RAG store ONCE at startup
# ===============================
rag = FaissStore(embed_texts)
rag.build()

# ===============================
# Intent keyword routing
# ===============================
KPI_TRIGGERS = [
    "performance",
    "percentage",
    "rate",
    "how are we doing",
    "what is our",
]

POLICY_TRIGGERS = [
    "what happens",
    "if",
    "should we",
    "what do we do",
    "action",
    "escalation",
]

# ===============================
# Chat Orchestrator
# ===============================
def chat(message: str) -> dict:
    msg = message.lower()

    # -------------------------------------------------
    # KPI PATH (metrics only — no policy questions)
    # -------------------------------------------------
    if (
        "on-time" in msg
        and any(k in msg for k in KPI_TRIGGERS)
        and not any(p in msg for p in POLICY_TRIGGERS)
    ):
        value = on_time_percentage(7)
        return {
            "answer": f"On-time delivery over the last 7 days is {value}%. Target is 92%.",
            "kpi": value,
            "mode": "kpi",
        }

    # -------------------------------------------------
    # RAG / POLICY PATH
    # -------------------------------------------------
    docs = rag.search(message)

    context = "\n\nContext:\n"
    sources = []

    for d in docs:
        context += f"[{d['source']}]\n{d['text']}\n\n"
        sources.append(d["source"])

    # -------------------------------------------------
    # OFFLINE MODE (no API key)
    # -------------------------------------------------
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "answer": (
                "Based on operating procedures, a drop below the on-time delivery target "
                "triggers escalation to dispatch review, route analysis, and carrier "
                "performance checks."
            ),
            "mode": "offline",
            "sources": sources,
        }

    # -------------------------------------------------
    # LLM PATH
    # -------------------------------------------------
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message + context},
        ],
        temperature=0.2,
    )

    return {
        "answer": response.choices[0].message.content,
        "mode": "llm",
        "sources": sources,
    }
