from pydantic import BaseModel, Field

from app.domain.enums import AdviceStatus, RiskPreference


class HoldingInput(BaseModel):
    symbol: str
    amount_cny: float = Field(..., ge=0)


class UserProfileInput(BaseModel):
    user_id: str = "demo-user"
    name: str | None = None
    investable_amount_cny: float | None = Field(default=None, ge=0)
    risk_preference: RiskPreference | None = None
    investment_horizon_months: int | None = Field(default=None, ge=1)
    target_market: str | None = None
    current_assets_cny: float | None = Field(default=None, ge=0)
    monthly_cash_need_cny: float = Field(default=0, ge=0)
    annual_fx_quota_usd: float = Field(default=50000, ge=0)
    used_fx_quota_usd: float = Field(default=0, ge=0)
    holdings: list[HoldingInput] = Field(default_factory=list)


class AdviceRequest(BaseModel):
    query: str = Field(..., min_length=3)
    profile: UserProfileInput


class RiskAssessmentOutput(BaseModel):
    score: int
    level: str
    suited_categories: list[str]
    rationale: list[str]


class PlanItemOutput(BaseModel):
    product_id: str
    product_name: str
    allocation_ratio: float
    region: str
    risk_level: int
    expected_return_band: str
    reasons: list[str]
    warnings: list[str]
    sources: list[str]


class PlanOutput(BaseModel):
    style: str
    summary: str
    estimated_max_drawdown_pct: float
    items: list[PlanItemOutput]
    compliance_status: str
    compliance_notes: list[str]


class ComplianceReportOutput(BaseModel):
    overall_status: str
    notes: list[str]
    checked_rules: list[str]


class AdviceResponse(BaseModel):
    request_id: str
    status: AdviceStatus
    message: str
    missing_fields: list[str] = Field(default_factory=list)
    risk_assessment: RiskAssessmentOutput | None = None
    plans: list[PlanOutput] = Field(default_factory=list)
    compliance_report: ComplianceReportOutput | None = None
    masked_profile: dict[str, str | float | int | None] = Field(default_factory=dict)
    workflow_trace: list[str] = Field(default_factory=list)
