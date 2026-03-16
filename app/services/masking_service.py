class MaskingService:
    def mask_profile(self, profile: dict) -> dict[str, str | float | int | None]:
        name = profile.get("name")
        investable_amount = profile.get("investable_amount_cny")
        current_assets = profile.get("current_assets_cny")

        return {
            "user_id": profile.get("user_id"),
            "name": self._mask_name(name),
            "investable_amount_cny": self._mask_amount(investable_amount),
            "current_assets_cny": self._mask_amount(current_assets),
            "risk_preference": profile.get("risk_preference"),
            "investment_horizon_months": profile.get("investment_horizon_months"),
            "target_market": profile.get("target_market"),
        }

    def _mask_name(self, name: str | None) -> str | None:
        if not name:
            return None
        return f"{name[0]}**"

    def _mask_amount(self, amount: float | int | None) -> str | None:
        if amount is None:
            return None
        if amount >= 10000:
            return f"{round(amount / 10000, 1)} 万元"
        return f"{amount} 元"
