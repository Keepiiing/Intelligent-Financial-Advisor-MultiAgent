from app.repositories.product_repository import ProductRepository
from app.services.market_data_service import MarketDataService


class KnowledgeService:
    def __init__(self, repository: ProductRepository, market_data_service: MarketDataService) -> None:
        self.repository = repository
        self.market_data_service = market_data_service

    def search_products(
        self,
        target_market: str | None,
        preferred_categories: list[str],
        risk_score: int,
    ) -> list[dict]:
        products = self.repository.list_products()
        ranked: list[tuple[int, dict]] = []

        for product in products:
            score = 0
            if target_market and product["region"] == target_market:
                score += 3
            if product["category"] in preferred_categories:
                score += 2

            score -= abs(product["risk_level"] - risk_score)

            snapshot = self.market_data_service.get_snapshot(product["id"])
            if snapshot["ytd_return_pct"] > 0:
                score += 1

            enriched = {**product, "market_snapshot": snapshot}
            ranked.append((score, enriched))

        ranked.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in ranked]
