from app.core import IPaymentGateway, IPaymentProcessor
from app.schemas import BasePaymentData, PaymentResponse


class CardPaymentProcessor(IPaymentProcessor):
    def __init__(self, stripe_gateway: IPaymentGateway):
        self.stripe_gateway = stripe_gateway
    
    def process(self, payment_data: BasePaymentData) -> PaymentResponse:
        payment_response = self.stripe_gateway.process_payment(payment_data)
        
        return payment_response