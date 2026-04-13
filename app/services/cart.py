from core import IShoppingCart, get_discount_strategy, STRATEGY_MAP
from schemas import AmountPurchasedModel, DiscountStrategy
from services.discounts import NoDiscount

class ShoppingCart(IShoppingCart):
    def calculate_total(
        self, amount_purchased: AmountPurchasedModel, discount_type: DiscountStrategy | str
        ) -> AmountPurchasedModel:
        """
        Apply a discount type to the purchase and calculate
        the total price.
        """
        discount_strategy = get_discount_strategy(discount_type, STRATEGY_MAP, default=NoDiscount())
        discount_value = discount_strategy.apply_discount(amount_purchased=amount_purchased)
        total_price = amount_purchased.amount - discount_value.amount
        
        return AmountPurchasedModel(
            amount=total_price
        )