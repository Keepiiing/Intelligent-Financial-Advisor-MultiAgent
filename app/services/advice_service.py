from app.orchestrator.workflow import AdvisorWorkflow
from app.schemas.advisor import AdviceRequest, AdviceResponse


class AdviceService:
    def __init__(self, workflow: AdvisorWorkflow) -> None:
        self.workflow = workflow

    def generate_advice(self, payload: AdviceRequest) -> AdviceResponse:
        final_state = self.workflow.invoke(payload)
        return AdviceResponse.model_validate(final_state["final_response"])
