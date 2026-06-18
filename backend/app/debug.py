def print_state_snapshot(state: dict) -> None:
    print("State snapshot")
    print("--------------")
    print(f"question_count: {state.get('question_count')}")
    print(f"waiting_for_patient: {state.get('waiting_for_patient')}")
    print(f"waiting_for_physician: {state.get('waiting_for_physician')}")
    print(f"diagnostic_summary exists: {bool(state.get('diagnostic_summary'))}")
    print(f"physician_treatment exists: {bool(state.get('physician_treatment'))}")
    print(f"final_report exists: {bool(state.get('final_report'))}")
