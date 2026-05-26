import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from openai import OpenAI
from app.rag.faiss_store import FaissStore
from app.rag.embeddings import embed_texts
from app.tools.kpi_tool import (
    total_revenue,
    average_revenue,
    total_loaded_miles,
    total_empty_miles,
    top_customers,
    top_routes,
    delayed_loads
)

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
    "on-time",
    "kpi",
    "late loads",
    "carrier score",
    "escalations",
    "performance",
    "trend",
    "percentage",
    "rate",
    "metrics"
]

POLICY_TRIGGERS = [
    "what happens",
    "if",
    "should we",
    "what do we do",
    "action",
    "escalation",
]
        
    
def chat(message: str) -> dict:
    msg = message.lower()

    # -----------------------------------
    # REVENUE
    # -----------------------------------

    if "revenue" in msg:

        return {
            "answer": str(total_revenue()),
            "mode": "kpi"
        }

    # -----------------------------------
    # TOP CUSTOMERS
    # -----------------------------------

    elif "top customers" in msg:

        data = top_customers()

        return {

            "answer": "Top customers by revenue.",

            "mode": "chart",

            "chart": {
                "type": "bar",

                "labels": [
                    item["customer"]
                    for item in data
                ],

                "values": [
                    item["revenue"]
                    for item in data
                ]
            }
        }

    # -----------------------------------
    # TOP ROUTES
    # -----------------------------------

    elif "top routes" in msg:

        data = top_routes()

        return {

            "answer": "Top revenue generating lanes.",

            "mode": "chart",

            "chart": {
                "type": "bar",

                "labels": [
                    item["route"]
                    for item in data
                ],

                "values": [
                    item["revenue"]
                    for item in data
                ]
            }
        }

    # -----------------------------------
    # DELAYED LOADS
    # -----------------------------------

    elif "delayed loads" in msg:

        data = delayed_loads()

        return {

            "answer": f"There are currently {data['delayed_loads']} delayed loads.",

            "mode": "kpi",

            "kpi": data["delayed_loads"]
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
