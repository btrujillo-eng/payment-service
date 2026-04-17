from core import IDiscountStrategy
from schemas import PaymentAmountModel
from decimal import Decimal

class NoDiscount(IDiscountStrategy):
    async def apply_discount(self, payment_amount: PaymentAmountModel) -> PaymentAmountModel:
        """
        Doesn't returns a discount value.
        """
        return PaymentAmountModel(transaction_amount=Decimal("0"))
    
class ChristmasDiscount(IDiscountStrategy):
    async def apply_discount(self, payment_amount: PaymentAmountModel) -> PaymentAmountModel:
        """
        Returns a discount value of 30%.
        """
        discount_value = payment_amount.transaction_amount * Decimal("0.30")
        return PaymentAmountModel(transaction_amount=Decimal(discount_value))
    
class FixedDiscount(IDiscountStrategy):
    async def apply_discount(self, payment_amount: PaymentAmountModel) -> PaymentAmountModel:
        """
        Returns a fixed discount value of 5000 if the purchase amount
        is greater than 15000. If purchase amount is less than 15000,
        doesn't return a discount value.
        """
        if payment_amount.transaction_amount >= Decimal("15000"):
            return PaymentAmountModel(transaction_amount=Decimal("5000"))
        return PaymentAmountModel(transaction_amount=Decimal("0"))
    
class BlackFridayDiscount(IDiscountStrategy):
    async def apply_discount(self, payment_amount: PaymentAmountModel) -> PaymentAmountModel:
        """
        Returns a discount value of 20%.
        """
        discount_value = payment_amount.transaction_amount * Decimal("0.20")
        return PaymentAmountModel(transaction_amount=discount_value)
    