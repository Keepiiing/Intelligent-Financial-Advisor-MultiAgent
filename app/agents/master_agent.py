import re

from app.agents.base import BaseAgent
from app.domain.state import AdviceState


class MasterAgent(BaseAgent):
    name = "master-agent"

    def run(self, state: AdviceState) -> AdviceState:
        query = state["query"]
        profile = state["profile"]
        extracted_slots = self._extract_slots(query)

        # Prefer explicit profile fields, then backfill from free-text extraction.
        merged_profile = {
            **profile,
            "investable_amount_cny": profile.get("investable_amount_cny") or extracted_slots.get("investable_amount_cny"),
            "risk_preference": profile.get("risk_preference") or extracted_slots.get("risk_preference"),
            "investment_horizon_months": profile.get("investment_horizon_months")
            or extracted_slots.get("investment_horizon_months"),
            "target_market": profile.get("target_market") or extracted_slots.get("target_market"),
        }

        missing_fields = []
        for field in ("investable_amount_cny", "risk_preference", "investment_horizon_months"):
            if not merged_profile.get(field):
                missing_fields.append(field)

        state["profile"] = merged_profile
        state["extracted_slots"] = extracted_slots
        state["missing_fields"] = missing_fields

        if missing_fields:
            self.add_trace(state, f"缺少关键信息: {', '.join(missing_fields)}")
        else:
            self.add_trace(state, "已完成意图识别、槽位提取和任务编排。")

        return state

    def _extract_slots(self, query: str) -> dict:
        slots: dict = {}

        amount_match = re.search(r"(\d+(?:\.\d+)?)\s*万", query)
        if amount_match:
            slots["investable_amount_cny"] = float(amount_match.group(1)) * 10000

        if "保守" in query or "低风险" in query or "稳健偏低" in query:
            slots["risk_preference"] = "conservative"
        elif "稳健" in query or "中等" in query or "均衡" in query:
            slots["risk_preference"] = "balanced"
        elif "进取" in query or "激进" in query or "高风险" in query:
            slots["risk_preference"] = "aggressive"

        month_match = re.search(r"(\d+)\s*(个月|月)", query)
        year_match = re.search(r"(\d+)\s*年", query)
        if month_match:
            slots["investment_horizon_months"] = int(month_match.group(1))
        elif year_match:
            slots["investment_horizon_months"] = int(year_match.group(1)) * 12

        if "海外" in query or "全球" in query or "美元" in query:
            slots["target_market"] = "overseas"
        elif "国内" in query or "境内" in query:
            slots["target_market"] = "domestic"

        return slots
