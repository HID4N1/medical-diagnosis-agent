# Demonstration Script

## Step 1: Start consultation

Open the React frontend or call `POST /consultation/start` with an initial
patient case. In LangGraph Studio, confirm the graph moves from `START` to
`supervisor`, then to `diagnostic_agent`.

## Step 2: Answer 5 questions

Submit each patient answer with `POST /consultation/resume`. After every
question generation, inspect the state and confirm `waiting_for_patient=True`.

## Step 3: Show MCP analysis

After the fifth patient answer, inspect `mcp_analysis` in Studio. Confirm the
detected symptoms, severity, red flags, and recommendation are visible.

## Step 4: Show physician interruption

Confirm the workflow pauses with `waiting_for_physician=True` and that
`physician_review_request` contains the synthèse clinique préliminaire and
recommandation intermédiaire.

## Step 5: Resume workflow
P
Submit the physician treatment with `POST /consultation/resume`. Confirm
`physician_treatment` is stored in the state and the graph resumes.

## Step 6: Generate final report

Inspect the final state and confirm `final_report` is populated by
`report_agent`.

## Step 7: Show disclaimer

Display the final report and confirm it includes:

`Ce système ne remplace pas une consultation médicale.`

## LangGraph Studio

Start Studio from the backend directory:

```bash
langgraph dev
```

Expected graph name:

`medical_graph`
