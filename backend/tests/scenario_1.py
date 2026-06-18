from scenario_utils import (
    assert_question_count,
    assert_report_generated,
    assert_waiting_for_physician_reached,
    run_consultation,
)


PATIENT_CASE = "Toux légère, fatigue et fièvre modérée"
ANSWERS = [
    "Depuis deux jours",
    "Oui",
    "4/10",
    "Aucun antécédent",
    "Aucun traitement",
]
PHYSICIAN_TREATMENT = "Repos et hydratation"


def run() -> None:
    result = run_consultation(PATIENT_CASE, ANSWERS, PHYSICIAN_TREATMENT)
    state = result["state"]

    assert_question_count(result["questions"])
    assert_waiting_for_physician_reached(state)
    assert_report_generated(state)


if __name__ == "__main__":
    run()
    print("PASS scenario_1")
