from uuid import uuid4

from app.agents.compliance_agent import ComplianceAgent
from app.agents.filter_agent import FilterAgent
from app.agents.master_agent import MasterAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.risk_agent import RiskAgent
from app.domain.state import AdviceState
from app.schemas.advisor import AdviceRequest

try:
    from langgraph.graph import END, StateGraph
except ImportError:  # pragma: no cover
    END = "__end__"
    StateGraph = None


class AdvisorWorkflow:
    def __init__(
        self,
        master_agent: MasterAgent,
        risk_agent: RiskAgent,
        recommendation_agent: RecommendationAgent,
        compliance_agent: ComplianceAgent,
        filter_agent: FilterAgent,
    ) -> None:
        self.master_agent = master_agent
        self.risk_agent = risk_agent
        self.recommendation_agent = recommendation_agent
        self.compliance_agent = compliance_agent
        self.filter_agent = filter_agent
        self.graph = self._build_graph()

    def _build_graph(self):
        if StateGraph is None:
            return None

        graph = StateGraph(AdviceState)
        graph.add_node("master", self.master_agent.run)
        graph.add_node("risk", self.risk_agent.run)
        graph.add_node("recommend", self.recommendation_agent.run)
        graph.add_node("compliance", self.compliance_agent.run)
        graph.add_node("filter", self.filter_agent.run)

        graph.set_entry_point("master")
        graph.add_conditional_edges(
            "master",
            self._route_after_master,
            {
                "filter": "filter",
                "risk": "risk",
            },
        )
        graph.add_edge("risk", "recommend")
        graph.add_edge("recommend", "compliance")
        graph.add_edge("compliance", "filter")
        graph.add_edge("filter", END)
        return graph.compile()

    def invoke(self, payload: AdviceRequest) -> AdviceState:
        initial_state: AdviceState = {
            "request_id": str(uuid4()),
            "query": payload.query,
            "profile": payload.profile.model_dump(mode="json"),
            "workflow_trace": [],
        }

        if self.graph is not None:
            return self.graph.invoke(initial_state)

        state = self.master_agent.run(initial_state)
        if state.get("missing_fields"):
            return self.filter_agent.run(state)
        state = self.risk_agent.run(state)
        state = self.recommendation_agent.run(state)
        state = self.compliance_agent.run(state)
        return self.filter_agent.run(state)

    def _route_after_master(self, state: AdviceState) -> str:
        return "filter" if state.get("missing_fields") else "risk"
