import os
from dotenv import load_dotenv

# =========================================
# LOAD ENV VARIABLES
# =========================================
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

# =========================================
# SYSTEM PROMPT
# =========================================
SYSTEM_PROMPT = """
You are FleetOps AI Assistant.

Rules:
- Use KPI data ONLY for metric questions.
- Use RAG documents for definitions, SOPs, and policy.
- Never invent numbers.
- Be concise, factual, and operational.
"""

# =========================================
# BUILD RAG STORE ONCE
# =========================================
rag = FaissStore(embed_texts)
rag.build()

# =========================================
# CHAT ORCHESTRATOR
# =========================================
def chat(message: str) -> dict:

    msg = message.lower()

    # =====================================================
    # TOP CUSTOMERS / REVENUE ANALYTICS
    # =====================================================

    if (

        "top customers" in msg
        or "top revenue customers" in msg
        or "customer revenue" in msg
        or "revenue analytics" in msg
        or "best customers" in msg
        or "show revenue analytics" in msg

    ):

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

    # =====================================================
    # TOP ROUTES
    # =====================================================

    elif (

        "top routes" in msg
        or "top lanes" in msg
        or "best routes" in msg
        or "best lanes" in msg

    ):

        data = top_routes()

        return {

            "answer": "Top revenue generating routes.",

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

    # =====================================================
    # TOTAL REVENUE
    # =====================================================

    elif (

        "revenue" in msg
        or "sales" in msg
        or "money" in msg
        or "gross revenue" in msg

    ):

        revenue_data = total_revenue()

        return {

            "answer": f"Total revenue is ${revenue_data['total_revenue']:,.2f}",

            "mode": "kpi",

            "kpi": revenue_data["total_revenue"]
        }

    # =====================================================
    # AVERAGE REVENUE
    # =====================================================

    elif (

        "average revenue" in msg
        or "avg revenue" in msg

    ):

        avg_data = average_revenue()

        return {

            "answer": f"Average revenue per load is ${avg_data['average_revenue']:,.2f}",

            "mode": "kpi",

            "kpi": avg_data["average_revenue"]
        }

    # =====================================================
    # LOADED MILES
    # =====================================================

    elif (

        "loaded miles" in msg
        or "total loaded miles" in msg

    ):

        loaded_data = total_loaded_miles()

        return {

            "answer": f"Total loaded miles: {loaded_data['loaded_miles']:,.0f}",

            "mode": "kpi",

            "kpi": loaded_data["loaded_miles"]
        }

    # =====================================================
    # EMPTY MILES
    # =====================================================

    elif (

        "empty miles" in msg
        or "deadhead" in msg

    ):

        empty_data = total_empty_miles()

        return {

            "answer": f"Total empty miles: {empty_data['empty_miles']:,.0f}",

            "mode": "kpi",

            "kpi": empty_data["empty_miles"]
        }

    # =====================================================
    # DELAYED LOADS
    # =====================================================

    elif (

        "delayed loads" in msg
        or "late loads" in msg
        or "delays" in msg

    ):

        delayed_data = delayed_loads()

        return {

            "answer": f"There are currently {delayed_data['delayed_loads']} delayed loads.",

            "mode": "kpi",

            "kpi": delayed_data["delayed_loads"]
        }

    # =====================================================
    # RAG / POLICY SEARCH
    # =====================================================

    docs = rag.search(message)

    context = "\n\nContext:\n"

    sources = []

    for d in docs:

        context += f"[{d['source']}]\n{d['text']}\n\n"

        sources.append(d["source"])

    # =====================================================
    # OFFLINE MODE
    # =====================================================

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        return {

            "answer": (
                "Based on operating procedures, a drop below the on-time "
                "delivery target triggers escalation to dispatch review, "
                "route analysis, and carrier performance checks."
            ),

            "mode": "offline",

            "sources": sources
        }

    # =====================================================
    # LLM MODE
    # =====================================================

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(

        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini"
        ),

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": message + context
            }

        ],

        temperature=0.2
    )

    return {

        "answer": response.choices[0].message.content,

        "mode": "llm",

        "sources": sources
    }