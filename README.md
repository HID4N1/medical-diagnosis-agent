# Medical Multi-Agent Diagnostic System

## Project Overview

This repository contains an academic medical multi-agent system for preliminary
clinical orientation. It demonstrates how LangGraph can orchestrate specialized
agents, how FastAPI can expose the workflow as an API, how MCP tools can provide
external decision-support data, and how a React frontend can guide a user through
the interaction.

The workflow is designed for education and demonstration only. It includes a
Human-in-the-Loop physician validation step before the final report is generated.

**This system does not replace a medical consultation.**

## Features

- Supervisor orchestration with LangGraph
- Diagnostic Agent for preliminary case analysis
- Five-question patient interview loop
- Human-in-the-Loop Physician Review
- Final structured report generation
- MCP medical tools for red flags, severity, and recommendations
- FastAPI backend API
- React frontend with Vite
- LangGraph Studio support
- Scenario validation scripts

## Architecture

```text
Patient
  ↓
Frontend
  ↓
FastAPI
  ↓
LangGraph
  ↓
MCP
  ↓
Physician Review
  ↓
Report Generation
```

Main workflow:

```text
START → Supervisor → DiagnosticAgent → Patient Loop
      → Supervisor → PhysicianReview → Supervisor → ReportAgent → END
```

Detailed diagrams are available in:

- `docs/architecture.md`
- `docs/workflow.md`

## Installation

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### MCP Server

```bash
cd mcp_server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

### LangGraph Studio

Studio uses `backend/langgraph.json` and is started from the backend directory:

```bash
cd backend
source .venv/bin/activate
langgraph dev
```

## API Endpoints

- `POST /consultation/start`
- `POST /consultation/resume`
- `GET /consultation/{thread_id}`
- `GET /consultation/{thread_id}/report`

Swagger UI:

```text
http://localhost:8000/docs
```

## Running Locally

Use the local run guide:

```text
docs/local_run_guide.md
```

Startup order:

1. MCP Server
2. Backend FastAPI
3. LangGraph Studio
4. React Frontend

## Test Scenarios

Scenario scripts are in `backend/tests/`.

Run all scenarios with the MCP server running:

```bash
cd backend
source .venv/bin/activate
python tests/run_all_scenarios.py
```

Included scenarios:

- Scenario 1: mild cough, fatigue, moderate fever
- Scenario 2: chest pain and difficulty breathing with high severity
- Scenario 3: mild fatigue and headache with low severity

## Documentation

- `docs/technical_report.md`
- `docs/demo_guide.md`
- `docs/demo_script.md`
- `docs/local_run_guide.md`
- `docs/project_structure.md`
- `docs/final_checklist.md`
- `docs/screenshots.md`

## Docker

Optional Docker support is available:

```bash
docker compose up --build
```

Local development with separate terminals remains the recommended demonstration
mode for LangGraph Studio.
