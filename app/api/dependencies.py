from functools import lru_cache

from app.agents.compliance_agent import ComplianceAgent
from app.agents.filter_agent import FilterAgent
from app.agents.master_agent import MasterAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.risk_agent import RiskAgent
from app.core.config import get_settings
from app.orchestrator.workflow import AdvisorWorkflow
from app.repositories.product_repository import ProductRepository
from app.services.advice_service import AdviceService
from app.services.compliance_service import ComplianceService
from app.services.knowledge_service import KnowledgeService
from app.services.market_data_service import MarketDataService
from app.services.masking_service import MaskingService


@lru_cache
def get_advice_service() -> AdviceService:
    settings = get_settings()
    repository = ProductRepository(settings.data_dir / "products.json")
    market_data_service = MarketDataService()
    knowledge_service = KnowledgeService(repository, market_data_service)
    compliance_service = ComplianceService(settings)
    masking_service = MaskingService()

    workflow = AdvisorWorkflow(
        master_agent=MasterAgent(),
        risk_agent=RiskAgent(),
        recommendation_agent=RecommendationAgent(knowledge_service),
        compliance_agent=ComplianceAgent(compliance_service),
        filter_agent=FilterAgent(masking_service),
    )
    return AdviceService(workflow)
