# Project Structure

```text
medical-diagnosis-agent/
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── schemas.py
│   │   ├── session_store.py
│   │   ├── nodes/
│   │   └── tools/
│   ├── tests/
│   ├── langgraph.json
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── routes/
│   ├── package.json
│   └── Dockerfile
├── mcp_server/
│   ├── server.py
│   ├── data/
│   │   └── red_flags.json
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── demo_guide.md
│   ├── demo_script.md
│   ├── final_checklist.md
│   ├── local_run_guide.md
│   ├── project_structure.md
│   ├── screenshots.md
│   ├── technical_report.md
│   └── workflow.md
├── docker-compose.yml
├── CHANGELOG.md
└── README.md
```

## Directory Purpose

- `backend/`: FastAPI application and LangGraph workflow.
- `backend/app/nodes/`: supervisor, diagnostic, physician review, and report nodes.
- `backend/app/tools/`: patient tools and MCP client.
- `backend/tests/`: scenario validation scripts.
- `frontend/`: React/Vite user interface.
- `mcp_server/`: FastMCP server and local red-flag dataset.
- `docs/`: academic documentation, diagrams, guides, and final checklist.
