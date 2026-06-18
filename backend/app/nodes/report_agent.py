from langchain_core.messages import AIMessage

from app.logger import logger
from app.state import MedicalState


DISCLAIMER = "Ce système ne remplace pas une consultation médicale."


def report_agent_node(state: MedicalState) -> dict:
    logger.info("Entering ReportAgent")
    physician_treatment = state.get("physician_treatment")
    if not physician_treatment:
        logger.info("ReportAgent -> waiting for physician treatment")
        return {
            "messages": [
                AIMessage(
                    content=(
                        "La revue par le médecin est requise avant la "
                        "génération du rapport final."
                    )
                )
            ]
        }

    patient_case = state.get("patient_case", "Cas patient non fourni.")
    patient_answers = state.get("patient_answers", [])
    diagnostic_summary = state.get(
        "diagnostic_summary",
        "Synthèse clinique préliminaire non disponible.",
    )
    interim_care = state.get(
        "interim_care",
        "Recommandation intermédiaire non disponible.",
    )
    answers_section = "\n".join(
        f"{index}. {answer}" for index, answer in enumerate(patient_answers, 1)
    )
    if not answers_section:
        answers_section = "Aucune réponse patient enregistrée."

    final_report = (
        "Cas initial patient\n"
        "-------------------\n"
        f"{patient_case}\n\n"
        "Réponses du patient\n"
        "-------------------\n"
        f"{answers_section}\n\n"
        "Synthèse clinique préliminaire\n"
        "------------------------------\n"
        f"{diagnostic_summary}\n\n"
        "Recommandation intermédiaire\n"
        "----------------------------\n"
        f"{interim_care}\n\n"
        "Conduite à tenir proposée par le médecin\n"
        "----------------------------------------\n"
        f"{physician_treatment}\n\n"
        "Note pédagogique et éthique\n"
        "---------------------------\n"
        "Ce rapport correspond à une simulation académique d'orientation "
        "clinique préliminaire. Il ne fournit pas de diagnostic définitif, "
        "de prescription, ni de conduite thérapeutique personnalisée.\n\n"
        f"{DISCLAIMER}"
    )
    logger.info("ReportAgent -> final_report generated")

    return {
        "final_report": final_report,
        "messages": [
            AIMessage(
                content="Le rapport final structuré a été généré."
            )
        ],
    }
