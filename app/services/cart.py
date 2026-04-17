from core import IShoppingCart, get_discount_strategy, STRATEGY_MAP
from schemas import PaymentAmountModel, DiscountStrategy
from services.discounts import NoDiscount

class ShoppingCart(IShoppingCart):
    async def calculate_total(
        self, amount_purchased: PaymentAmountModel, discount_type: DiscountStrategy | str
        ) -> PaymentAmountModel:
        """
        Apply a discount type to the purchase and calculate
        the total price.
        """
        discount_strategy = await get_discount_strategy(discount_type, STRATEGY_MAP, default=NoDiscount())
        discount_value = discount_strategy.apply_discount(payment_amount=amount_purchased)
        total_price = amount_purchased.transaction_amount - discount_value.transaction_amount
        
        return PaymentAmountModel(
            transaction_amount=total_price
        )