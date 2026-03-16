from app.agents.base import BaseAgent
from app.domain.enums import AdviceStatus
from app.domain.state import AdviceState
from app.services.masking_service import MaskingService


class FilterAgent(BaseAgent):
    name = "filter-agent"

    def __init__(self, masking_service: MaskingService) -> None:
        self.masking_service = masking_service

    def run(self, state: AdviceState) -> AdviceState:
        missing_fields = state.get("missing_fields", [])
        masked_profile = self.masking_service.mask_profile(state["profile"])

        if missing_fields:
            self.add_trace(state, "因关键信息缺失，输出补参提示。")
            state["final_response"] = {
                "request_id": state["request_id"],
                "status": AdviceStatus.needs_more_info,
                "message": "缺少生成投资建议所需的关键字段，请先补充用户画像信息。",
                "missing_fields": missing_fields,
                "risk_assessment": None,
                "plans": [],
                "compliance_report": None,
                "masked_profile": masked_profile,
                "workflow_trace": state.get("workflow_trace", []),
            }
            return state

        compliance_status = state["compliance_report"]["overall_status"]
        response_status = (
            AdviceStatus.manual_review if compliance_status == "manual_review" else AdviceStatus.success
        )

        if response_status == AdviceStatus.manual_review:
            message = "建议先进入人工复核。"
        elif compliance_status == "needs_adjustment":
            message = "已生成投资建议，但部分组合需要结合合规意见微调。"
        else:
            message = "已生成可解释的投资建议。"

        self.add_trace(state, "已完成脱敏和最终响应组装。")
        state["final_response"] = {
            "request_id": state["request_id"],
            "status": response_status,
            "message": message,
            "missing_fields": [],
            "risk_assessment": state["risk_assessment"],
            "plans": state["candidate_plans"],
            "compliance_report": state["compliance_report"],
            "masked_profile": masked_profile,
            "workflow_trace": state.get("workflow_trace", []),
        }
        return state
