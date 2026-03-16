from app.agents.base import BaseAgent
from app.domain.state import AdviceState


class RiskAgent(BaseAgent):
    name = "risk-agent"

    def run(self, state: AdviceState) -> AdviceState:
        profile = state["profile"]
        reasons: list[str] = []

        risk_preference = profile["risk_preference"]
        base_score = {"conservative": 3, "balanced": 6, "aggressive": 8}[risk_preference]
        reasons.append(f"基于用户风险偏好 {risk_preference} 设置基础风险分。")

        investable_amount = float(profile.get("investable_amount_cny") or 0)
        if investable_amount >= 1_000_000:
            base_score += 1
            reasons.append("可投资金额较高，风险承受能力上调。")
        elif investable_amount <= 100_000:
            base_score -= 1
            reasons.append("可投资金额较低，风险承受能力下调。")

        horizon = int(profile.get("investment_horizon_months") or 12)
        if horizon >= 36:
            base_score += 1
            reasons.append("投资期限较长，可接受更多波动。")
        elif horizon <= 12:
            base_score -= 1
            reasons.append("投资期限较短，需要控制波动。")

        monthly_cash_need = float(profile.get("monthly_cash_need_cny") or 0)
        if investable_amount and monthly_cash_need / investable_amount >= 0.2:
            base_score -= 1
            reasons.append("流动性需求较高，适合降低风险敞口。")

        score = max(1, min(10, round(base_score)))

        if score <= 3:
            level = "保守型"
            suited_categories = ["cash", "bond", "fixed_income"]
        elif score <= 6:
            level = "均衡型"
            suited_categories = ["bond", "mixed", "global_income"]
        else:
            level = "进取型"
            suited_categories = ["equity", "global_equity", "sector_growth"]

        state["risk_assessment"] = {
            "score": score,
            "level": level,
            "suited_categories": suited_categories,
            "rationale": reasons,
        }
        self.add_trace(state, f"完成风险评估，结果为 {level}（{score}/10）。")
        return state
