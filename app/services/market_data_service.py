class MarketDataService:
    def __init__(self) -> None:
        self._snapshots = {
            "global-dividend-fund": {"nav": 1.234, "ytd_return_pct": 9.8, "fx_note": "USD/CNY 7.20"},
            "asia-growth-fund": {"nav": 1.087, "ytd_return_pct": 12.4, "fx_note": "USD/CNY 7.20"},
            "usd-bond-income-fund": {"nav": 1.018, "ytd_return_pct": 4.1, "fx_note": "USD/CNY 7.20"},
            "global-tech-select-fund": {"nav": 1.562, "ytd_return_pct": 16.7, "fx_note": "USD/CNY 7.20"},
            "domestic-bond-plus-fund": {"nav": 1.045, "ytd_return_pct": 5.2, "fx_note": "CNY assets"},
            "cash-management-fund": {"nav": 1.003, "ytd_return_pct": 2.0, "fx_note": "CNY assets"},
        }

    def get_snapshot(self, product_id: str) -> dict:
        return self._snapshots.get(
            product_id,
            {"nav": 1.0, "ytd_return_pct": 0.0, "fx_note": "sample data"},
        )
