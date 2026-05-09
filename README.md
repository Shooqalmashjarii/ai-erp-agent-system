# 🏢 Multi-Agent ERP System

An intelligent, agent-driven ERP assistant built with **LangChain**, **Gemini 2.5 Flash**, and **SQLite** — enabling natural language queries across sales, inventory, and analytics data through a modular multi-agent architecture.

> **Graduation Project — Khalifa University**

---

## 🧠 System Architecture

```
User Query (Natural Language)
        ↓
   Router Agent  ←── Intent Classifier (LLM-powered)
        ↓
   ┌────┴─────────────┐
Sales Agent   Inventory Agent   Analytics Agent
   ↓                ↓                  ↓
NL → SQL       Stock Queries     Trends & Insights
   ↓                ↓                  ↓
        SQLite ERP Database (erp.db)
        ↓
  Streamlit Frontend
```

---

## ✨ Features

- **Router Agent** — classifies user intent and delegates to the right specialist agent
- **Sales Agent** — handles revenue, orders, and customer queries via NL-to-SQL
- **Inventory Agent** — tracks stock levels, suppliers, and warehouse insights
- **Analytics Agent** — generates higher-level trends, regional analysis, and recommendations
- **Conversation Memory** — agents remember context for follow-up queries
- **Streamlit Frontend** — clean UI for interacting with the system
- **MCP-Compliant Architecture** — modular, pluggable, single-responsibility agents

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Gemini 2.5 Flash (Google) |
| Agent Framework | LangChain + AgentExecutor |
| Database | SQLite (ERP schema) |
| Frontend | Streamlit |
| Language | Python 3 |

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

### 3. Run the system
```bash
python main.py
streamlit run frontend.py
```

### 4. Example queries
```
"Who are the top 5 customers by total order value?"
"Show the most recent 10 sales orders"
"What is the total sales revenue this quarter?"
"Which products are low on stock?"
"Show regional sales trends"
```

---

## 📁 Project Structure

```
multi-agent-erp/
├── main.py                  # Router agent + entry point
├── frontend.py              # Streamlit UI
├── llm_setup.py             # LLM configuration
├── build_llm.py             # LLM builder utility
├── db.py                    # Database connection
├── requirements.txt
├── agents/
│   ├── router_agent.py      # Intent classification + delegation
│   ├── salesAgent.py        # Sales & order queries
│   ├── inventory_agent.py   # Stock & supplier queries
│   ├── analyticsAgent.py    # Trends & recommendations
│   └── agents_llm_setup.py
└── db/
    └── erp.db               # SQLite ERP database
```

---

## 💡 Key Learnings

- Designing modular multi-agent systems with clear separation of concerns
- Natural language to SQL translation using LLM reasoning
- LangChain AgentExecutor, memory management, and tool encapsulation
- Building production-like AI systems with pluggable architecture

---

## 👩‍💻 Author

**Shooq Al Mashjari** — Computer Engineering Student, Khalifa University
[LinkedIn](http://www.linkedin.com/in/shooq-al-mashjari-521b85353)
