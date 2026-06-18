# Local Run Guide

Academic medical multi-agent project using FastAPI, LangGraph, LangChain,
FastMCP, React, Vite, and LangGraph Studio.

## Required Tools

- Python 3.10+
- Node.js 18+
- npm

## Startup Order

Use four separate terminals and start services in this order:

1. MCP Server
2. Backend FastAPI
3. LangGraph Studio
4. React Frontend

## 1. MCP Server

Terminal 1:

```bash
cd mcp_server
source .venv/bin/activate
python server.py
```

Expected MCP URL:

```text
http://localhost:23000/mcp
```

Optional MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

## 2. Backend FastAPI

Terminal 2:

```bash
cd backend
source .venv/bin/activate
uvicorn app.api:app --reload
```

Expected backend URL:

```text
http://localhost:8000
```

Swagger URL:

```text
http://localhost:8000/docs
```

## 3. LangGraph Studio

Terminal 3:

```bash
cd backend
source .venv/bin/activate
langgraph dev
```

LangGraph Studio reads:

```text
backend/langgraph.json
```

It must contain:

```json
{
  "dependencies": ["./"],
  "graphs": {
    "medical_graph": "./app/graph.py:graph"
  },
  "env": "./.env"
}
```

Expected graph name:

```text
medical_graph
```

## 4. React Frontend

Terminal 4:

```bash
cd frontend
npm install
npm run dev
```

Expected frontend URL:

```text
http://localhost:5173
```

## Full Test Scenario

Open the frontend:

```text
http://localhost:5173
```

Initial case:

```text
Patient avec toux légère, fatigue et fièvre modérée depuis deux jours.
```

Five patient answers:

```text
Depuis deux jours.
Oui, fièvre modérée.
Douleur évaluée à 4 sur 10.
Aucun antécédent important.
Aucun traitement actuel.
```

Physician treatment:

```text
Repos, hydratation, surveillance clinique et consultation rapide en cas d’aggravation.
```

Expected result:

```text
Ce système ne remplace pas une consultation médicale.
```

The final report should contain that disclaimer.

## Troubleshooting

### MCP Connection Error

Check that the MCP server is running:

```text
http://localhost:23000/mcp
```

Restart it:

```bash
cd mcp_server
source .venv/bin/activate
python server.py
```

### Backend Cannot Connect To MCP

Start the MCP server before the backend.

Confirm the MCP client points to:

```text
http://localhost:23000/mcp
```

Then restart the backend:

```bash
cd backend
source .venv/bin/activate
uvicorn app.api:app --reload
```

### Frontend Cannot Reach Backend

Check that FastAPI is running:

```text
http://localhost:8000/docs
```

Confirm the frontend API base URL is:

```text
http://localhost:8000
```

### LangGraph Studio Does Not Show Graph

Run Studio from the backend directory:

```bash
cd backend
source .venv/bin/activate
langgraph dev
```

Verify `backend/langgraph.json` contains `medical_graph` and points to:

```text
./app/graph.py:graph
```

### Port Already In Use

Find the process using the port:

```bash
lsof -i :23000
lsof -i :8000
lsof -i :5173
lsof -i :2024
```

Stop the old process, then restart the service.

### Virtual Environment Not Activated

If commands like `uvicorn`, `langgraph`, or package imports fail, activate the
right environment first:

```bash
cd backend
source .venv/bin/activate
```

or:

```bash
cd mcp_server
source .venv/bin/activate
```
