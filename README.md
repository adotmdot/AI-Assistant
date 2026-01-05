# FleetOps AI Assistant

FleetOps AI Assistant is a production-style AI system designed for logistics and fleet operations teams.  
It answers **KPI-based performance questions using authoritative metrics** and **operational or policy questions using internal documentation** via Retrieval-Augmented Generation (RAG).

This project demonstrates how enterprise AI assistants are built, governed, and deployed in real-world environments.

---

## 🚚 Problem This Solves

Logistics teams often:
- Waste time digging through dashboards for KPIs
- Interpret metrics inconsistently
- Lack fast access to operational procedures and escalation rules

FleetOps AI Assistant solves this by:
- Routing KPI questions to **trusted metric functions**
- Routing policy questions to **approved internal documents**
- Enforcing guardrails so numbers are **never hallucinated**

---

## ✨ Key Features

### ✅ KPI-Aware Intelligence
- On-time delivery performance
- SLA threshold awareness
- Escalation triggers based on targets

### 📚 RAG-Based Policy Answers
- KPI definitions
- Escalation playbooks
- Operating procedures (SOPs)

### 🔐 Enterprise Guardrails
- KPI values come **only** from metric functions
- LLM is **blocked** from inventing numbers
- Separate logic paths for metrics vs documents

### 🚀 Production-Ready API
- FastAPI backend
- Dockerized
- Swagger UI included
- Designed for Azure deployment

---

## 🧠 System Architecture

```
User
 │
 ▼
FastAPI (/chat endpoint)
 │
 ├── KPI Router
 │     └── Metric Functions (authoritative data)
 │
 └── RAG Router
       └── Vector Search (FAISS)
             └── LLM (document-grounded)
```

---

## 🛠 Technology Stack

### Backend
- Python 3.12
- FastAPI
- Uvicorn

### AI / ML
- OpenAI API
- FAISS Vector Store
- Embeddings for document retrieval
- Retrieval-Augmented Generation (RAG)

### Cloud & DevOps
- Docker
- Azure Container Apps
- Azure Container Registry (ACR)
- Azure CLI

### Tooling
- Swagger UI
- Environment-based configuration

---

## 📂 Project Structure

```
app/
├─ main.py
├─ chat/
│  └─ orchestrator.py
├─ rag/
│  ├─ faiss_store.py
│  └─ embeddings.py
├─ tools/
│  └─ kpi_tool.py
└─ data/
   └─ docs/
```

---

## 🚀 Local Development

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Start the API
```bash
uvicorn app.main:app --reload
```

### 3️⃣ Verify health
```text
http://localhost:8000/health
```

### 4️⃣ Open Swagger UI
```text
http://localhost:8000/docs
```

---

## 🧪 Example API Requests

### KPI Question
```json
{
  "message": "What is our on-time delivery performance?"
}
```

Response uses **real KPI logic**, not LLM guesses.

---

### Policy Question
```json
{
  "message": "What happens if on-time delivery drops below target?"
}
```

Response is grounded in **internal documentation** using RAG.

---

## ☁️ Azure Deployment Overview

The application is designed for deployment using:

- **Azure Container Registry** for image storage
- **Azure Container Apps** for hosting
- **Log Analytics** for observability

Deployment benefits:
- Serverless scaling
- Secure environment variables
- Enterprise-grade logging
- HTTPS by default

---

## 🔒 Guardrail Design

This system enforces:
- No numeric hallucinations
- Clear KPI vs Policy separation
- Read-only document grounding
- Deterministic metric calculations

This mirrors real enterprise AI governance models.

---

## 🎥 Demo Walkthrough (Suggested Script)

> “This is FleetOps AI Assistant, an AI-powered logistics assistant built using FastAPI, RAG, and Azure Container Apps.
>
> KPI-related questions are routed to authoritative metric functions, while operational questions are answered using internal documentation through vector search.
>
> Guardrails ensure the system never invents numbers, which is critical for business decision-making.
>
> The entire application is containerized and deployed to Azure, demonstrating how AI assistants are built and operated in enterprise environments.”

---

## 📌 Use Cases

- Logistics performance monitoring
- Fleet operations analytics
- SOP & escalation guidance
- Internal AI assistant prototypes
- Portfolio demonstration of enterprise AI

---

## 👤 Author

**Anthony Massaquoi**  
BS Software Engineering (in progress)  
AI Engineering • Cloud • Backend Systems

---

## 📎 Disclaimer

This project is a technical demonstration and does not use real company data.
