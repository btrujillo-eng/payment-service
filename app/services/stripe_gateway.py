from schemas import PaymentData, PaymentResponse, PaymentAmountModel
from core import IPaymentGateway,to_stripe_amount, get_processing_network

from datetime import datetime, timezone
from stripe import StripeError
from dotenv import load_dotenv
from decimal import Decimal
from typing import cast
import logging
import stripe
import os

_ = load_dotenv()

logger = logging.getLogger(__name__)

class StripeGateway(IPaymentGateway):
    async def process_payment(self, payment_data: PaymentData) -> PaymentResponse:
        stripe.api_key = os.getenv('STRIPE_API_KEY')
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
                transaction_amount=Decimal(charge["amount"])
            )
            
        except StripeError as e:
            logger.critical(f"The transaction with ID 5566 was rejected due to problems with the Stripe gateway | Error: {e}", stack_info=True)
            return PaymentResponse(
                currency=charge["currency"],
                payment_method_id=charge["source"],
                transaction_id=charge["id"],
                payment_status=charge["status"],
                created_at=datetime.fromtimestamp(charge["created"], tz=timezone.utc),
                message="Estamos teniendo problemas para procesar el pago. Por favor intenta más tarde",
                transaction_amount=Decimal(charge["amount"])
            )