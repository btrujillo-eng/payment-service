from app.schemas import PaymentAmountModel

async def to_stripe_amount(payment_amount: PaymentAmountModel) -> int:
    """
    It's responsible for transferring the payment amount to Stripe in the requested format.
    """
    return int(payment_amount.transaction_amount * 100)