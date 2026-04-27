from app.core import IPaymentProcessor, IPaymentGateway, ICardValidator
from app.schemas import CardPaymentData, PaymentResponse
from app.errors import CardPaymentProcessorError

class CardPaymentProcessor(IPaymentProcessor):
    def __init__(self, card_validator: ICardValidator, stripe_gateway: IPaymentGateway):
        self.card_validator = card_validator
        self.stripe_gateway = stripe_gateway
    
    async def process(self, payment_data: CardPaymentData) -> PaymentResponse:
        valid_card = await self.card_validator.validate(payment_data.card_number)
        if not valid_card:
            raise CardPaymentProcessorError("The card is not valide")
        payment_response = await self.stripe_gateway.process_payment(payment_data)
        
        return payment_response