from enum import Enum


class RiskPreference(str, Enum):
    conservative = "conservative"
    balanced = "balanced"
    aggressive = "aggressive"


class AdviceStatus(str, Enum):
    success = "success"
    needs_more_info = "needs_more_info"
    manual_review = "manual_review"
