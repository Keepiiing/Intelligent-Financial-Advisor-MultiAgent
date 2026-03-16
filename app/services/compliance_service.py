from app.core.config import Settings


class ComplianceService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def evaluate_plan(self, profile: dict, plan: dict, risk_score: int) -> tuple[str, list[str]]:
        notes: list[str] = []
        status = "approved"

        investable_amount = float(profile.get("investable_amount_cny") or 0)
        fx_quota = float(profile.get("annual_fx_quota_usd") or self.settings.default_fx_limit_usd)
        used_fx_quota = float(profile.get("used_fx_quota_usd") or 0)
        remaining_fx_quota = max(fx_quota - used_fx_quota, 0)

        overseas_ratio = sum(
            item["allocation_ratio"] for item in plan["items"] if item["region"] == "overseas"
        )
        required_fx_usd = (investable_amount * overseas_ratio / 100) / self.settings.usd_cny_rate

        if required_fx_usd > remaining_fx_quota:
            status = "needs_adjustment"
            notes.append(
                f"海外资产预计占用购汇额度 {required_fx_usd:.0f} USD，超过剩余额度 {remaining_fx_quota:.0f} USD。"
            )

        max_product_risk = max(item["risk_level"] for item in plan["items"])
        if max_product_risk > risk_score:
            status = "needs_adjustment"
            notes.append("组合中存在高于用户承受等级的产品，需要重新筛选。")

        current_assets = float(profile.get("current_assets_cny") or 0)
        if any(item["risk_level"] >= 8 for item in plan["items"]) and current_assets < 1_000_000:
            status = "manual_review"
            notes.append("高风险产品仅建议总资产不低于 100 万的用户购买。")

        if not notes:
            notes.append("外汇额度、风险匹配、产品适格性校验通过。")

        return status, notes
