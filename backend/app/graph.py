import sys
from uuid import uuid4

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.nodes.diagnostic_agent import (
    add_patient_answer,
    diagnostic_agent_node,
    diagnostic_router,
)
from app.nodes.physician_review import (
    add_physician_treatment,
    physician_review_node,
)
from app.nodes.report_agent import report_agent_node
from app.nodes.supervisor import route_supervisor, supervisor_node
from app.state import MedicalState


def physician_review_router(state: MedicalState) -> str:
    if state.get("waiting_for_physician"):
        return "WAIT"

    return "COMPLETE"


workflow = StateGraph(MedicalState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("diagnostic_agent", diagnostic_agent_node)
workflow.add_node("physician_review", physician_review_node)
workflow.add_node("report_agent", report_agent_node)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "diagnostic_agent": "diagnostic_agent",
        "physician_review": "physician_review",
        "report_agent": "report_agent",
        "FINISH": END,
    },
)
workflow.add_conditional_edges(
    "diagnostic_agent",
    diagnostic_router,
    {
        "WAIT": END,
        "COMPLETE": "supervisor",
        "CONTINUE": "diagnostic_agent",
    },
)
workflow.add_conditional_edges(
    "physician_review",
    physician_review_router,
    {
        "WAIT": END,
        "COMPLETE": "supervisor",
    },
)
workflow.add_edge("report_agent", "supervisor")

memory = MemorySaver()


def _running_under_langgraph_api() -> bool:
    return any(module_name.startswith("langgraph_api") for module_name in sys.modules)


graph = (
    workflow.compile()
    if _running_under_langgraph_api()
    else workflow.compile(checkpointer=memory)
)


def thread_config(thread_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": thread_id,
        }
    }


def visualize_graph():
    from IPython.display import Image, display

    display(
        Image(
            graph.get_graph().draw_mermaid_png()
        )
    )


def run_demo():
    demo_thread_id = str(uuid4())
    result = graph.invoke(
        {
            "patient_case": (
                "Patient avec toux légère, fatigue et fièvre modérée depuis "
                "deux jours."
            ),
            "messages": [],
            "question_count": 0,
            "patient_answers": [],
        },
        config=thread_config(demo_thread_id),
    )
    return result


def run_questionnaire_demo():
    demo_thread_id = str(uuid4())
    state = {
        "patient_case": "Patient avec toux et fatigue.",
        "messages": [],
        "question_count": 0,
        "patient_answers": [],
    }

    state = graph.invoke(state, config=thread_config(demo_thread_id))
    print(f"Question #1: {state['current_question']}")

    simulated_answers = [
        "Depuis deux jours.",
        "Oui, fièvre modérée sans frissons importants.",
        "Inconfort évalué à 4 sur 10.",
        "Aucun antécédent médical important connu.",
        "Aucun traitement actuellement.",
    ]

    for answer in simulated_answers:
        state = add_patient_answer(state, answer)
        state = graph.invoke(state, config=thread_config(demo_thread_id))
        if state.get("waiting_for_patient"):
            question_number = state.get("question_count", 0) + 1
            print(f"Question #{question_number}: {state['current_question']}")

    return state


def run_physician_review_demo():
    demo_thread_id = str(uuid4())
    state = {
        "patient_case": (
            "Patient avec toux, fatigue et fièvre modérée depuis deux jours."
        ),
        "messages": [],
        "question_count": 0,
        "patient_answers": [],
    }

    state = graph.invoke(state, config=thread_config(demo_thread_id))
    print(f"Question #1: {state['current_question']}")

    simulated_answers = [
        "Depuis deux jours.",
        "Oui, fièvre modérée.",
        "Inconfort évalué à 4 sur 10.",
        "Aucun antécédent médical important connu.",
        "Aucun traitement actuellement.",
    ]

    for answer in simulated_answers:
        state = add_patient_answer(state, answer)
        state = graph.invoke(state, config=thread_config(demo_thread_id))
        if state.get("waiting_for_patient"):
            question_number = state.get("question_count", 0) + 1
            print(f"Question #{question_number}: {state['current_question']}")

    if state.get("waiting_for_physician"):
        print("Revue médecin requise.")
        print(state["physician_review_request"])

    state = add_physician_treatment(
        state,
        (
            "Surveillance clinique, hydratation, repos, et consultation "
            "rapide en cas d'aggravation."
        ),
    )
    state = graph.invoke(state, config=thread_config(demo_thread_id))

    return state


if __name__ == "__main__":
    result = run_physician_review_demo()
    print(result["final_report"])
