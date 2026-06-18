# Demonstration Guide

Target duration: 5-7 minutes.

## 1. Start MCP Server

```bash
cd mcp_server
source .venv/bin/activate
python server.py
```

Expected URL:

```text
http://localhost:23000/mcp
```

## 2. Start FastAPI Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.api:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## 3. Start LangGraph Studio

```bash
cd backend
source .venv/bin/activate
langgraph dev
```

Open the Studio URL printed in the terminal and select:

```text
medical_graph
```

## 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## 5. Enter Patient Case

Use:

```text
Patient avec toux légère, fatigue et fièvre modérée depuis deux jours.
```

Explain that this starts an academic clinical-orientation workflow.

## 6. Answer Questions

Enter the five patient answers:

```text
Depuis deux jours.
Oui, fièvre modérée.
Douleur évaluée à 4 sur 10.
Aucun antécédent important.
Aucun traitement actuel.
```

In Studio, show `question_count`, `patient_answers`, and
`waiting_for_patient`.

## 7. Physician Review

Show the physician review page. Explain that the workflow pauses with:

```text
waiting_for_physician=True
```

Enter:

```text
Repos, hydratation, surveillance clinique et consultation rapide en cas d’aggravation.
```

## 8. Generate Report

Submit the physician treatment and show the final report page.

In Studio, show:

- `physician_treatment`
- `final_report`
- `mcp_analysis`

## 9. Display Final Result

Confirm that the final report contains:

```text
Ce système ne remplace pas une consultation médicale.
```
