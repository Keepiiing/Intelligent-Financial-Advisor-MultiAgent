from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_advice() -> None:
    payload = {
        "query": "我有50万本金，风险中等，想投资海外基金，投资周期24个月",
        "profile": {
            "user_id": "demo-user",
            "name": "张三",
            "investable_amount_cny": 500000,
            "risk_preference": "balanced",
            "investment_horizon_months": 24,
            "target_market": "overseas",
            "current_assets_cny": 1200000,
            "monthly_cash_need_cny": 15000,
            "annual_fx_quota_usd": 50000,
            "used_fx_quota_usd": 10000,
        },
    }

    response = client.post("/api/v1/advice", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["status"] in {"success", "manual_review"}
    assert body["risk_assessment"]["score"] >= 1
    assert len(body["plans"]) == 3
    assert body["workflow_trace"]


def test_generate_advice_with_missing_fields() -> None:
    payload = {
        "query": "想要海外基金建议",
        "profile": {"user_id": "demo-user"},
    }

    response = client.post("/api/v1/advice", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "needs_more_info"
    assert "investable_amount_cny" in body["missing_fields"]
