from core import IDiscountStrategy
from schemas import AmountPurchasedModel
from decimal import Decimal

class NoDiscount(IDiscountStrategy):
    def apply_discount(self, amount_purchased: AmountPurchasedModel) -> AmountPurchasedModel:
        """
        Doesn't returns a discount value.
        """
        return AmountPurchasedModel( amount=Decimal("0"))
    
class ChristmasDiscount(IDiscountStrategy):
    def apply_discount(self, amount_purchased: AmountPurchasedModel) -> AmountPurchasedModel:
        """
        Returns a discount value of 30%.
        """
        discount_value = amount_purchased.amount * Decimal("0.30")
        return AmountPurchasedModel( amount=Decimal(discount_value))
    
class FixedDiscount(IDiscountStrategy):
    def apply_discount(self, amount_purchased: AmountPurchasedModel) -> AmountPurchasedModel:
        """
        Returns a fixed discount value of 5000 if the purchase amount
        is greater than 15000. If purchase amount is less than 15000,
        doesn't return a discount value.
        """
        if amount_purchased.amount >= Decimal("15000"):
            return AmountPurchasedModel( amount=Decimal("5000"))
        return AmountPurchasedModel( amount=Decimal("0"))
    
class BlackFridayDiscount(IDiscountStrategy):
    def apply_discount(self, amount_purchased: AmountPurchasedModel) -> AmountPurchasedModel:
        """
        Returns a discount value of 20%.
        """
        discount_value = amount_purchased.amount * Decimal("0.20")
        return AmountPurchasedModel( amount=discount_value)
    