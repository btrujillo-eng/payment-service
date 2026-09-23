from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_default_discount,
    get_process_payment,
    get_strategy_map,
)
from app.core import IDiscountStrategy
from app.errors import CardPaymentProcessorError, NotificationServiceError
from app.schemas import CardPaymentData, DiscountStrategy, PaymentResponse
from app.use_cases import ProcessPaymentUseCase

router = APIRouter(prefix="/payments", tags=["payments"])
@router.post("/", response_model=PaymentResponse)
async def process_payment(
    payment_data: CardPaymentData,
    process_payment: ProcessPaymentUseCase = Depends(get_process_payment),
    strategy_map: dict[DiscountStrategy, IDiscountStrategy] = Depends(get_strategy_map), 
    default_discount: IDiscountStrategy = Depends(get_default_discount)
    ) -> PaymentResponse:
    try:
        return process_payment.process(payment_data, strategy_map, default_discount)
    except CardPaymentProcessorError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY  , detail=str(e)
        )
    except NotificationServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )   
        