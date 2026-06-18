from scenario_utils import (
    assert_question_count,
    assert_report_generated,
    run_consultation,
)


PATIENT_CASE = "Fatigue légère et maux de tête"
ANSWERS = [
    "Trois jours",
    "Non",
    "2/10",
    "Aucun",
    "Aucun",
]
PHYSICIAN_TREATMENT = "Surveillance simple"


def run() -> None:
    result = run_consultation(PATIENT_CASE, ANSWERS, PHYSICIAN_TREATMENT)
    state = result["state"]
    analysis = state.get("mcp_analysis", {})

    assert_question_count(result["questions"])
    assert_report_generated(state)

    if analysis.get("severity") != "low":
        raise AssertionError(
            f"Expected low severity, got {analysis.get('severity')}."
        )


if __name__ == "__main__":
    run()
    print("PASS scenario_3")
