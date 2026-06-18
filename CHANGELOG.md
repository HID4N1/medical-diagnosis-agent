# Changelog

## Phase 1 Setup

- Created the base project structure.
- Prepared backend, frontend, MCP server, and documentation directories.

## Phase 2 LangGraph

- Implemented the shared `MedicalState`.
- Created the LangGraph workflow.
- Added supervisor-based routing.

## Phase 3 Patient Loop

- Added the Diagnostic Agent.
- Implemented the five-question patient interview loop.
- Stored patient answers and question count in graph state.

## Phase 4 Human Review

- Added Physician Review as a Human-in-the-Loop step.
- Implemented workflow interruption and resume behavior for physician treatment.

## Phase 5 FastAPI

- Exposed consultation endpoints.
- Added session management.
- Added state and report retrieval endpoints.

## Phase 6 MCP

- Created the FastMCP medical server.
- Added red-flag, severity, and recommendation tools.
- Integrated MCP analysis into the Diagnostic Agent.

## Phase 7 Frontend

- Added React/Vite frontend.
- Created consultation pages for start, questions, physician review, and report.
- Added API client, context, routing, and academic medical styling.

## Phase 8 Validation

- Added LangGraph Studio configuration.
- Added logging and state snapshot helpers.
- Added scenario validation scripts.
- Validated graph visibility, interruptions, resume behavior, MCP analysis, and final reports.

## Phase 9 Packaging

- Added final README.
- Added technical report.
- Added architecture and workflow diagrams.
- Added screenshot placeholders.
- Added demonstration guide.
- Added project structure document.
- Added final validation checklist.
- Added Docker and Docker Compose support.
- Added `.env.example` files.
