from uuid import uuid4


SESSIONS = {}


def create_session() -> str:
    thread_id = str(uuid4())
    SESSIONS[thread_id] = {}
    return thread_id


def get_session(thread_id: str) -> dict:
    if thread_id not in SESSIONS:
        raise KeyError(thread_id)

    return SESSIONS[thread_id]


def save_session(thread_id: str, state: dict) -> None:
    SESSIONS[thread_id] = state


def session_exists(thread_id: str) -> bool:
    return thread_id in SESSIONS
