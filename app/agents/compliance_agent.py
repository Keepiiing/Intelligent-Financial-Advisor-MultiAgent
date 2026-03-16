from app.agents.base import BaseAgent
from app.domain.state import AdviceState
from app.services.compliance_service import ComplianceService


class ComplianceAgent(BaseAgent):
    name = "compliance-agent"

    def __init__(self, compliance_service: ComplianceService) -> None:
        self.compliance_service = compliance_service

    def run(self, state: AdviceState) -> AdviceState:
        profile = state["profile"]
        risk_score = state["risk_assessment"]["score"]
        plans = []
        overall_notes: list[str] = []
        statuses = set()

        for plan in state["candidate_plans"]:
            status, notes = self.compliance_service.evaluate_plan(profile, plan, risk_score)
            statuses.add(status)
            overall_notes.extend(notes)
            plans.append({**plan, "compliance_status": status, "compliance_notes": notes})

        if "manual_review" in statuses:
            overall_status = "manual_review"
        elif "needs_adjustment" in statuses:
            overall_status = "needs_adjustment"
        else:
            overall_status = "approved"

        state["candidate_plans"] = plans
        state["compliance_report"] = {
            "overall_status": overall_status,
            "notes": sorted(set(overall_notes)),
            "checked_rules": ["外汇额度校验", "风险匹配校验", "产品适格性校验"],
        }
        self.add_trace(state, f"已完成合规校验，整体状态为 {overall_status}。")
        return state
