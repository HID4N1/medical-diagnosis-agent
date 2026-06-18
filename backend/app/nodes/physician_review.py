from langchain_core.messages import AIMessage

from app.logger import logger
from app.state import MedicalState


def _format_patient_answers(patient_answers: list[str]) -> str:
    if not patient_answers:
        return "Aucune réponse patient enregistrée."

    return "\n".join(
        f"{index}. {answer}" for index, answer in enumerate(patient_answers, 1)
    )


def physician_review_node(state: MedicalState) -> dict:
    logger.info("Entering PhysicianReview")
    if not state.get("physician_treatment"):
        patient_case = state.get("patient_case", "Cas patient non fourni.")
        patient_answers = _format_patient_answers(state.get("patient_answers", []))
        diagnostic_summary = state.get(
            "diagnostic_summary",
            "Synthèse clinique préliminaire non disponible.",
        )
        interim_care = state.get(
            "interim_care",
            "Recommandation intermédiaire non disponible.",
        )

        physician_review_request = (
            "Revue médecin requise\n"
            "---------------------\n"
            "Ce contenu provient d'une simulation académique et ne constitue "
            "pas un dispositif médical.\n\n"
            "Cas initial patient\n"
            "-------------------\n"
            f"{patient_case}\n\n"
            "Réponses du patient\n"
            "-------------------\n"
            f"{patient_answers}\n\n"
            "Synthèse clinique préliminaire\n"
            "------------------------------\n"
            f"{diagnostic_summary}\n\n"
            "Recommandation intermédiaire\n"
            "----------------------------\n"
            f"{interim_care}"
        )
        logger.info("PhysicianReview -> waiting_for_physician")

        return {
            "physician_review_request": physician_review_request,
            "waiting_for_physician": True,
            "messages": [
                AIMessage(
                    content=(
                        "La synthèse clinique préliminaire est prête pour "
                        "revue par le médecin traitant."
                    )
                )
            ],
        }

    logger.info("PhysicianReview -> physician_treatment recorded")
    return {
        "waiting_for_physician": False,
        "messages": [
            AIMessage(
                content=(
                    "La conduite à tenir proposée par le médecin a été "
                    "enregistrée."
                )
            )
        ],
    }


def add_physician_treatment(state: MedicalState, treatment: str) -> MedicalState:
    logger.info("PhysicianReview received physician treatment")
    return {
        **state,
        "physician_treatment": treatment,
        "waiting_for_physician": False,
    }
