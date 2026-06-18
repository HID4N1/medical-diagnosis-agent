from pydantic import BaseModel


class SessionStartResponse(BaseModel):
    thread_id: str


class StartConsultationRequest(BaseModel):
    patient_case: str


class StartConsultationResponse(BaseModel):
    thread_id: str
    status: str
    question: str | None = None
    review_request: str | None = None
    final_report: str | None = None


class ResumeConsultationRequest(BaseModel):
    thread_id: str
    answer: str | None = None
    physician_treatment: str | None = None


class ConsultationStateResponse(BaseModel):
    thread_id: str
    state: dict


class ReportResponse(BaseModel):
    thread_id: str
    final_report: str | None = None
    status: str
