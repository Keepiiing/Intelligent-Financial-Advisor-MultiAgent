from app.agents.base import BaseAgent
from app.domain.state import AdviceState
from app.services.knowledge_service import KnowledgeService


class RecommendationAgent(BaseAgent):
    name = "recommendation-agent"

    def __init__(self, knowledge_service: KnowledgeService) -> None:
        self.knowledge_service = knowledge_service

    def run(self, state: AdviceState) -> AdviceState:
        profile = state["profile"]
        risk_score = state["risk_assessment"]["score"]
        preferred_categories = state["risk_assessment"]["suited_categories"]
        target_market = profile.get("target_market")

        ranked_products = self.knowledge_service.search_products(
            target_market=target_market,
            preferred_categories=preferred_categories,
            risk_score=risk_score,
        )

        plans = [
            self._build_plan("保守方案", ranked_products, max(risk_score - 2, 2)),
            self._build_plan("均衡方案", ranked_products, risk_score),
            self._build_plan("进取方案", ranked_products, min(risk_score + 2, 9)),
        ]
        state["candidate_plans"] = plans
        self.add_trace(state, "已生成保守、均衡、进取三套候选组合。")
        return state

    def _build_plan(self, style: str, ranked_products: list[dict], target_risk: int) -> dict:
        selected = [
            product for product in ranked_products if abs(product["risk_level"] - target_risk) <= 2
        ][:2]

        if len(selected) < 2:
            selected = ranked_products[:2]

        allocations = [60, 40] if style != "进取方案" else [55, 45]

        items = []
        for product, ratio in zip(selected, allocations):
            snapshot = product["market_snapshot"]
            items.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "allocation_ratio": ratio,
                    "region": product["region"],
                    "risk_level": product["risk_level"],
                    "expected_return_band": product["expected_return_band"],
                    "reasons": [
                        f"产品风险等级 {product['risk_level']} 与目标风险 {target_risk} 接近。",
                        f"年内收益表现 {snapshot['ytd_return_pct']}%，适合作为组合候选。",
                    ],
                    "warnings": product["warnings"],
                    "sources": [
                        "sample_product_knowledge_base",
                        f"market_snapshot_nav={snapshot['nav']}",
                        snapshot["fx_note"],
                    ],
                }
            )

        avg_risk = sum(item["risk_level"] for item in items) / len(items)

        return {
            "style": style,
            "summary": f"{style}优先匹配风险等级约 {target_risk} 的产品组合。",
            "estimated_max_drawdown_pct": round(avg_risk * 2.3, 1),
            "items": items,
        }
