from core import IPaymentPocessor
from schemas import AmountPurchasedModel, DiscountStrategy

class PaymentProcessorService(IPaymentPocessor):
    def __init__(self):
        pass
    
    def process(
        self, payment_method: str, discount_type: DiscountStrategy | str, 
        amount_purchased: AmountPurchasedModel
        ) -> str:
        ...