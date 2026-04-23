from app.core import IShoppingCart, IDiscountStrategy, get_discount_strategy
from app.schemas import PaymentAmountModel, DiscountStrategy

from typing import Dict

class ShoppingCart(IShoppingCart):
    async def calculate_total(
        self, payment_amount: PaymentAmountModel, discount_type: DiscountStrategy | str,
        strategy_map: Dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy
        ) -> PaymentAmountModel:
        """
        Apply a discount type to the purchase and calculate
        the total price.
        """
        discount_strategy = await get_discount_strategy(discount_type, strategy_map, default=default_discount)
        discount_value = await discount_strategy.apply_discount(payment_amount=payment_amount)
        total_price = payment_amount.transaction_amount - discount_value.transaction_amount
        
        return PaymentAmountModel(
            transaction_amount=total_price
        )