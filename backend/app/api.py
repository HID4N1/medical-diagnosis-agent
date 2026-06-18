from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.graph import graph, thread_config
from app.nodes.diagnostic_agent import add_patient_answer
from app.nodes.physician_review import add_physician_treatment
from app.schemas import (
    ConsultationStateResponse,
    ReportResponse,
    ResumeConsultationRequest,
    SessionStartResponse,
    StartConsultationRequest,
    StartConsultationResponse,
)
from app.session_store import (
    create_session,
    get_session,
    save_session,
    session_exists,
)


app = FastAPI(
    title="Medical Multi-Agent LangGraph API",
    description="Academic clinical-orientation simulation. Not a medical device.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_response(thread_id: str, state: dict) -> dict:
    if state.get("waiting_for_patient") is True:
        return {
            "thread_id": thread_id,
            "status": "waiting_patient",
            "question": state.get("current_question"),
        }

    if state.get("waiting_for_physician") is True:
        return {
            "thread_id": thread_id,
            "status": "waiting_physician",
            "review_request": state.get("physician_review_request"),
        }

    if state.get("final_report"):
        return {
            "thread_id": thread_id,
            "status": "completed",
            "final_report": state.get("final_report"),
        }

    return {
        "thread_id": thread_id,
        "status": "running",
    }


def serialize_state(state: dict) -> dict:
    serialized = dict(state)
    messages = serialized.get("messages")

    if messages is not None:
        serialized["messages"] = [
            message.content if hasattr(message, "content") else str(message)
            for message in messages
        ]

    return serialized


def _get_existing_session(thread_id: str) -> dict:
    try:
        return get_session(thread_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Session not found.") from exc


@app.post("/sessions/start", response_model=SessionStartResponse)
def start_session() -> dict:
    thread_id = create_session()
    return {"thread_id": thread_id}


@app.post("/consultation/start", response_model=StartConsultationResponse)
def start_consultation(request: StartConsultationRequest) -> dict:
    thread_id = create_session()
    initial_state = {
        "patient_case": request.patient_case,
        "messages": [],
        "question_count": 0,
        "patient_answers": [],
        "waiting_for_patient": False,
        "waiting_for_physician": False,
    }

    state = graph.invoke(initial_state, config=thread_config(thread_id))
    save_session(thread_id, state)

    return build_response(thread_id, state)


@app.post("/consultation/resume", response_model=StartConsultationResponse)
def resume_consultation(request: ResumeConsultationRequest) -> dict:
    if not session_exists(request.thread_id):
        raise HTTPException(status_code=404, detail="Session not found.")

    state = get_session(request.thread_id)

    if state.get("waiting_for_patient") is True:
        if not request.answer:
            raise HTTPException(
                status_code=400,
                detail="Patient answer is required to resume this consultation.",
            )

        updated_state = add_patient_answer(state, request.answer)
        state = graph.invoke(updated_state, config=thread_config(request.thread_id))
        save_session(request.thread_id, state)
        return build_response(request.thread_id, state)

    if state.get("waiting_for_physician") is True:
        if not request.physician_treatment:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Physician treatment is required to resume this consultation."
                ),
            )

        updated_state = add_physician_treatment(
            state,
            request.physician_treatment,
        )
        state = graph.invoke(updated_state, config=thread_config(request.thread_id))
        save_session(request.thread_id, state)
        return build_response(request.thread_id, state)

    raise HTTPException(
        status_code=400,
        detail="Consultation is not waiting for patient or physician input.",
    )


@app.get("/consultation/{thread_id}", response_model=ConsultationStateResponse)
def get_consultation(thread_id: str) -> dict:
    state = _get_existing_session(thread_id)
    return {
        "thread_id": thread_id,
        "state": serialize_state(state),
    }


@app.get("/consultation/{thread_id}/report", response_model=ReportResponse)
def get_report(thread_id: str) -> dict:
    state = _get_existing_session(thread_id)
    final_report = state.get("final_report")

    if final_report:
        return {
            "thread_id": thread_id,
            "status": "completed",
            "final_report": final_report,
        }

    return {
        "thread_id": thread_id,
        "status": "not_ready",
        "final_report": None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
