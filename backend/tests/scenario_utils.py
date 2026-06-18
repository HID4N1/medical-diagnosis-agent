import sys
from pathlib import Path
from uuid import uuid4

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.graph import graph, thread_config
from app.nodes.diagnostic_agent import add_patient_answer
from app.nodes.physician_review import add_physician_treatment


def run_consultation(patient_case: str, answers: list[str], physician: str) -> dict:
    thread_id = str(uuid4())
    config = thread_config(thread_id)
    questions = []

    state = graph.invoke(
        {
            "patient_case": patient_case,
            "messages": [],
            "question_count": 0,
            "patient_answers": [],
            "waiting_for_patient": False,
            "waiting_for_physician": False,
        },
        config=config,
    )

    for answer in answers:
        if not state.get("waiting_for_patient"):
            raise AssertionError("Graph did not pause for patient input.")

        questions.append(state.get("current_question"))
        state = add_patient_answer(state, answer)
        state = graph.invoke(state, config=config)

    if not state.get("waiting_for_physician"):
        raise AssertionError("Graph did not pause for physician review.")

    state = add_physician_treatment(state, physician)
    state = graph.invoke(state, config=config)

    return {
        "state": state,
        "questions": questions,
        "thread_id": thread_id,
    }


def assert_report_generated(state: dict) -> None:
    if not state.get("final_report"):
        raise AssertionError("Final report was not generated.")


def assert_question_count(questions: list[str], expected: int = 5) -> None:
    if len(questions) != expected:
        raise AssertionError(
            f"Expected {expected} questions, got {len(questions)}."
        )


def assert_waiting_for_physician_reached(state: dict) -> None:
    if not state.get("physician_review_request"):
        raise AssertionError("Physician review request was not generated.")
