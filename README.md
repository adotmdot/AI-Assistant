# FleetOps AI Assistant

FleetOps AI Assistant is a full-stack AI-powered logistics analytics platform designed for fleet operations and transportation teams.

The application combines:
- AI-powered operational assistance
- KPI-driven analytics
- Interactive business dashboards
- Retrieval-Augmented Generation (RAG)
- Enterprise API architecture
- Cloud-ready deployment

FleetOps AI Assistant demonstrates how modern enterprise AI systems are built using FastAPI, React, vector search, analytics visualization, and cloud-native infrastructure.

---

# 🚚 Problem This Solves

Logistics and fleet operations teams often struggle with:

- Slow access to KPI metrics
- Fragmented reporting systems
- Inconsistent operational answers
- Manual dashboard analysis
- Difficulty accessing SOPs and escalation procedures
- Lack of centralized analytics visibility

FleetOps AI Assistant solves this by providing:

✅ Real-time KPI analytics  
✅ AI-powered operational guidance  
✅ Interactive business dashboards  
✅ Retrieval-based document intelligence  
✅ Enterprise-grade API orchestration  
✅ Visual analytics and charting

---

# ✨ Key Features

## 📊 Interactive Analytics Dashboard
- React + Vite frontend
- Enterprise dashboard UI
- Responsive analytics layout
- Dynamic chart rendering
- KPI visualization cards
- Currency-formatted metrics
- Multi-colored analytics charts
- Custom chart legends
- Mobile-friendly dashboard

---

## 🧠 AI-Powered Operations Assistant
- Natural language logistics queries
- KPI-aware routing system
- RAG-based operational guidance
- Context-aware AI responses
- Enterprise AI orchestration

---

## 📈 KPI Analytics
Supports analytics such as:

- Total revenue
- Average revenue
- Delayed loads
- Top customers
- Top revenue routes
- Loaded miles
- Empty miles
- Operational performance metrics

---

## 📚 RAG-Based Knowledge Retrieval
The assistant can answer questions using:

- Internal SOP documents
- Escalation procedures
- Operational policies
- KPI definitions
- Logistics guidance documentation

Powered by:
- FAISS vector database
- Embedding search
- Retrieval-Augmented Generation (RAG)

---

## 🔐 Enterprise Guardrails
FleetOps AI Assistant enforces:

- KPI responses only from authoritative functions
- No hallucinated business metrics
- Deterministic metric calculations
- Separate KPI vs policy routing
- Controlled document grounding

---

## ☁️ Cloud-Ready Architecture
Built for deployment using:

- Docker
- Azure Container Apps
- Azure Container Registry
- FastAPI APIs
- Environment-based configuration

---

# 🧠 System Architecture

```text
React Frontend Dashboard
        │
        ▼
FastAPI Backend API
        │
        ├── KPI Router
        │      └── Metric Functions
        │
        └── RAG Router
               └── FAISS Vector Search
                      └── OpenAI LLM
```

---

# 🛠 Technology Stack

## Frontend
- React
- Vite
- Recharts
- Axios
- Responsive CSS

## Backend
- Python 3.12
- FastAPI
- Uvicorn

## AI / ML
- OpenAI API
- FAISS Vector Store
- Vector Embeddings
- Retrieval-Augmented Generation (RAG)

## Cloud & DevOps
- Docker
- Azure Container Apps
- Azure Container Registry
- Azure CLI

## Tooling
- Swagger UI
- GitHub
- Environment Configuration

---

# 📂 Project Structure

```text
app/
├── main.py
├── chat/
│   └── orchestrator.py
├── rag/
│   ├── faiss_store.py
│   └── embeddings.py
├── tools/
│   └── kpi_tool.py
├── models/
├── load.py
├── seed_data.py
└── data/

frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── public/
└── package.json
```

---

# 📊 Dashboard Features

The FleetOps dashboard provides:

- Interactive analytics charts
- Revenue KPI cards
- Delayed load monitoring
- Top customer analytics
- Revenue route visualizations
- Currency-formatted charts
- Dynamic legends
- Hover analytics tooltips
- Responsive enterprise UI
- Real-time API-driven responses

Charts are dynamically rendered using Recharts and powered directly by FastAPI backend responses.

---

# 📈 Example Queries

Users can ask questions such as:

- "Show top customers by revenue"
- "Display top routes"
- "What is total revenue?"
- "How many delayed loads are there?"
- "Show revenue analytics"
- "What happens if delivery targets are missed?"
- "Show operational performance trends"

---

# 🚀 Local Development

## Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start Vite frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# 🧪 Example API Requests

## KPI Query

```json
{
  "message": "Show top customers by revenue"
}
```

---

## Policy Query

```json
{
  "message": "What happens if delivery targets are missed?"
}
```

---

# ☁️ Azure Deployment Overview

FleetOps AI Assistant is designed for enterprise cloud deployment using Azure services.

## Azure Services Used
- Azure Container Apps
- Azure Container Registry (ACR)
- Azure Log Analytics
- Azure CLI

## Deployment Benefits
- HTTPS by default
- Containerized infrastructure
- Scalable API hosting
- Enterprise logging
- Secure environment variables
- Cloud-native architecture

---

# 🔒 Guardrail Design

This system enforces enterprise AI governance principles:

- No hallucinated KPI metrics
- Deterministic business calculations
- Read-only document grounding
- KPI vs policy routing separation
- Controlled analytics generation

This mirrors real-world enterprise AI assistant architecture.

---

# 🎥 Demo Overview

FleetOps AI Assistant demonstrates:

✅ Full-stack engineering  
✅ AI orchestration systems  
✅ Analytics visualization  
✅ KPI intelligence  
✅ Retrieval-Augmented Generation  
✅ API architecture  
✅ Cloud deployment readiness  
✅ Enterprise dashboard design

---

# 📌 Use Cases

- Logistics analytics
- Fleet operations monitoring
- Transportation KPI tracking
- AI-powered operations assistants
- SOP guidance systems
- Business analytics dashboards
- Enterprise AI prototypes
- Portfolio demonstration projects

---

# 👤 Author

## Anthony Massaquoi

Full-Stack Software Engineer  
AI Engineering • Cloud • Data Analytics • Backend Systems

BS Software Engineering (In Progress)

---

# 📎 Disclaimer

This project is a technical demonstration project created for educational, portfolio, and enterprise AI architecture demonstration purposes.

No real company or proprietary logistics data is used.
