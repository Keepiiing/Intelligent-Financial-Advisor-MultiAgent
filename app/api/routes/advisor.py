from fastapi import APIRouter, Depends

from app.api.dependencies import get_advice_service
from app.schemas.advisor import AdviceRequest, AdviceResponse
from app.services.advice_service import AdviceService

router = APIRouter(tags=["advisor"])


@router.post("/advice", response_model=AdviceResponse, summary="Generate investment advice")
def create_advice(
    payload: AdviceRequest,
    service: AdviceService = Depends(get_advice_service),
) -> AdviceResponse:
    return service.generate_advice(payload)
