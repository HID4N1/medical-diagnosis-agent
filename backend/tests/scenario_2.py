from scenario_utils import (
    assert_question_count,
    assert_report_generated,
    assert_waiting_for_physician_reached,
    run_consultation,
)


PATIENT_CASE = "Chest pain and difficulty breathing"
ANSWERS = [
    "Depuis une heure",
    "Non",
    "8/10",
    "Hypertension",
    "Aucun traitement",
]
PHYSICIAN_TREATMENT = "Consultation urgente"


def run() -> None:
    result = run_consultation(PATIENT_CASE, ANSWERS, PHYSICIAN_TREATMENT)
    state = result["state"]
    analysis = state.get("mcp_analysis", {})
    red_flags = analysis.get("red_flags", {}).get("red_flags_detected", [])

    assert_question_count(result["questions"])
    assert_waiting_for_physician_reached(state)
    assert_report_generated(state)

    if not red_flags:
        raise AssertionError("Expected MCP red flags to be detected.")

    if analysis.get("severity") != "high":
        raise AssertionError(
            f"Expected high severity, got {analysis.get('severity')}."
        )


if __name__ == "__main__":
    run()
    print("PASS scenario_2")
