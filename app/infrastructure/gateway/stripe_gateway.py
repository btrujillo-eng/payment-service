from schemas import PaymentData, PaymentResponse, PaymentAmountModel
from core import IPaymentGateway,to_stripe_amount, get_processing_network

from datetime import datetime, timezone
from stripe import StripeError
from decimal import Decimal
from typing import cast
from uuid import uuid4
import logging
import stripe


logger = logging.getLogger(__name__)

class StripeGateway(IPaymentGateway):
    """
    This is a Stripe payment gateway.
    
    It is responsible for payment processing and returning the payment details. Any 
    class that implement this payment gateway can define the 'process_payment' method.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    async def process_payment(self, payment_data: PaymentData) -> PaymentResponse:
        """
        It's responsible for processing a payment and returning the payment details.
        """
        stripe.api_key = self.api_key
        amount = await to_stripe_amount(PaymentAmountModel(transaction_amount=payment_data.transaction_amount))
        source = await get_processing_network(payment_data.card_number)
        source = cast(str, source)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency=payment_data.currency,
                source=source,
                description=f"Charge for {payment_data.user_data.first_name} {payment_data.user_data.first_surname}"
            )
            
            logger.info(f"Payment sucessful | Transaction id: {charge["id"]}")
            return PaymentResponse(
                currency=charge["currency"],
                payment_method_id=charge["source"],
                transaction_id=charge["id"],
                payment_status=charge["status"],
                created_at=datetime.fromtimestamp(charge["created"], tz=timezone.utc),
                message="Pago exitoso",
                card_number=payment_data.card_number,
                transaction_amount=Decimal(charge["amount"])
            )
            
        except StripeError as e:
            logger.critical(f"The transaction failed for {payment_data.user_data.first_name} | Error: {e}", stack_info=True)
            return PaymentResponse(
                currency=payment_data.currency,
                payment_method_id="error",
                transaction_id=uuid4(),
                payment_status="failed",
                created_at=datetime.today(),
                message="Estamos teniendo problemas para procesar el pago. Por favor intenta más tarde",
                card_number=payment_data.card_number,
                transaction_amount=payment_data.transaction_amount
            )