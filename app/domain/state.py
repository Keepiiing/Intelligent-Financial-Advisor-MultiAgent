from typing import Any, TypedDict


class AdviceState(TypedDict, total=False):
    request_id: str
    query: str
    profile: dict[str, Any]
    extracted_slots: dict[str, Any]
    missing_fields: list[str]
    workflow_trace: list[str]
    risk_assessment: dict[str, Any]
    candidate_plans: list[dict[str, Any]]
    compliance_report: dict[str, Any]
    final_response: dict[str, Any]
