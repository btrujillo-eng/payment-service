from core import IPaymentProcessor
from schemas import PaymentAmountModel, DiscountStrategy

class PaymentProcessorService(IPaymentProcessor):
    def __init__(self):
        pass
    
    async def process(
        self, payment_method: str, discount_type: DiscountStrategy | str, 
        amount_purchased: PaymentAmountModel
        ) -> str:
        ...