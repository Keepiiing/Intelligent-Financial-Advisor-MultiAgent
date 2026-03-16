from app.domain.state import AdviceState


class BaseAgent:
    name = "base-agent"

    def run(self, state: AdviceState) -> AdviceState:
        raise NotImplementedError

    def add_trace(self, state: AdviceState, message: str) -> None:
        state.setdefault("workflow_trace", []).append(f"{self.name}: {message}")
