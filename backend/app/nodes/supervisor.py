from app.state import MedicalState
from app.logger import logger


def supervisor_node(state: MedicalState) -> dict:
    if not state.get("diagnostic_summary"):
        logger.info("Supervisor -> diagnostic_agent")
        return {"next": "diagnostic_agent"}

    if not state.get("physician_treatment"):
        logger.info("Supervisor -> physician_review")
        return {"next": "physician_review"}

    if not state.get("final_report"):
        logger.info("Supervisor -> report_agent")
        return {"next": "report_agent"}

    logger.info("Supervisor -> FINISH")
    return {"next": "FINISH"}


def route_supervisor(state: MedicalState) -> str:
    logger.info("Supervisor route selected: %s", state["next"])
    return state["next"]
