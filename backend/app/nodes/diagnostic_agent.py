import asyncio

from langchain_core.messages import AIMessage

from app.logger import logger
from app.state import MedicalState
from app.tools.mcp_client import analyze_symptoms
from app.tools.patient_tools import ask_patient


SYMPTOM_KEYWORDS = {
    "difficulty breathing": ["difficulty breathing", "shortness of breath", "dyspnea", "essoufflement", "difficulté à respirer", "difficulte a respirer"],
    "chest pain": ["chest pain", "douleur thoracique", "douleur poitrine"],
    "fatigue": ["fatigue", "fatigué", "fatiguee"],
    "headache": ["headache", "mal de tête", "mal de tete", "céphalée", "cephalee"],
    "high fever": ["high fever", "forte fièvre", "forte fievre", "fièvre", "fievre", "fever"],
    "loss of consciousness": ["loss of consciousness", "perte de connaissance", "perte de conscience", "évanouissement", "evanouissement"],
}


def add_patient_answer(state: MedicalState, answer: str) -> MedicalState:
    logger.info("DiagnosticAgent received patient answer")
    patient_answers = list(state.get("patient_answers", []))
    patient_answers.append(answer)

    return {
        **state,
        "patient_answers": patient_answers,
        "question_count": state.get("question_count", 0) + 1,
        "waiting_for_patient": False,
    }


def extract_symptoms(patient_case: str, patient_answers: list[str]) -> list[str]:
    corpus = " ".join([patient_case, *patient_answers]).lower()
    symptoms = []

    for symptom, keywords in SYMPTOM_KEYWORDS.items():
        if any(keyword in corpus for keyword in keywords):
            symptoms.append(symptom)

    return symptoms


def diagnostic_agent_node(state: MedicalState) -> dict:
    logger.info("Entering DiagnosticAgent")
    patient_case = state.get("patient_case", "Cas patient non fourni.")
    question_count = state.get("question_count", 0)
    patient_answers = state.get("patient_answers", [])
    logger.info("Question count: %s", question_count)

    if question_count < 5:
        question_number = question_count + 1
        question = ask_patient(question_number, patient_case)
        logger.info("DiagnosticAgent -> waiting_for_patient")

        return {
            "current_question": question,
            "waiting_for_patient": True,
            "question_count": question_count,
            "patient_answers": patient_answers,
            "messages": [
                AIMessage(
                    content=(
                        f"Question {question_number}/5 au patient : {question}"
                    )
                )
            ],
        }

    symptoms = extract_symptoms(patient_case, patient_answers)
    logger.info("Extracted symptoms: %s", symptoms)
    analysis = asyncio.run(analyze_symptoms(symptoms))
    red_flags_detected = analysis.get("red_flags", {}).get(
        "red_flags_detected",
        [],
    )
    red_flags_label = (
        ", ".join(item["symptom"] for item in red_flags_detected)
        if red_flags_detected
        else "aucun"
    )
    severity = analysis.get("severity", "low")
    recommendation = analysis.get(
        "recommendation",
        "Surveillance simple recommandée.",
    )

    diagnostic_summary = (
        "Synthèse clinique préliminaire basée sur le cas initial et les "
        "réponses fournies par le patient. "
        "Cette synthèse ne constitue pas un diagnostic définitif.\n\n"
        f"Cas initial: {patient_case}\n\n"
        "Réponses patient:\n"
        + "\n".join(
            f"{index}. {answer}" for index, answer in enumerate(patient_answers, 1)
        )
        + "\n\n"
        "Analyse complémentaire par outils MCP de support décisionnel:\n"
        f"- Symptômes repérés: {', '.join(symptoms) if symptoms else 'aucun'}\n"
        f"- Niveau de sévérité observé: {severity}\n"
        f"- Signaux d'alerte détectés: {red_flags_label}\n\n"
        "Orientation clinique préliminaire: les informations fournies peuvent "
        "servir de base à une discussion pédagogique et à une évaluation "
        "médicale ultérieure par un professionnel qualifié. Cette synthèse "
        "ne constitue pas un diagnostic médical."
    )
    interim_care = f"Recommandation intermédiaire : {recommendation}"
    logger.info("Diagnostic summary generated")

    return {
        "diagnostic_summary": diagnostic_summary,
        "interim_care": interim_care,
        "mcp_analysis": analysis,
        "waiting_for_patient": False,
        "messages": [
            AIMessage(
                content=(
                    "Synthèse clinique préliminaire et recommandation "
                    "intermédiaire générées. "
                    "Elle est uniquement pédagogique et ne constitue pas un "
                    "diagnostic définitif."
                )
            )
        ],
        "question_count": question_count,
        "patient_answers": patient_answers,
    }


def diagnostic_router(state: MedicalState) -> str:
    if state.get("waiting_for_patient") is True:
        logger.info("DiagnosticAgent router -> WAIT")
        return "WAIT"

    if state.get("diagnostic_summary"):
        logger.info("DiagnosticAgent router -> COMPLETE")
        return "COMPLETE"

    logger.info("DiagnosticAgent router -> CONTINUE")
    return "CONTINUE"
