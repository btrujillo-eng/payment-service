from decimal import Decimal

from app.core import (
    DiscountStrategy,
    IDiscountStrategy,
    IShoppingCart,
    get_discount_strategy,
)


class ShoppingCart(IShoppingCart):
    def calculate_total(
        self, payment_amount: Decimal, discount_type: DiscountStrategy | str,
        strategy_map: dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy
        ) -> Decimal:
        """
        Apply a discount type to the purchase and calculate
        the total price.
        """
        discount_strategy = get_discount_strategy(discount_type, strategy_map, default=default_discount)
        discount_value =  discount_strategy.apply_discount(payment_amount=payment_amount)
        total_price = payment_amount - discount_value
        
        return Decimal(total_price)