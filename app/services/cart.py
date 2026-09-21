from app.core import IDiscountStrategy, IShoppingCart, get_discount_strategy
from app.schemas import DiscountStrategy, PaymentAmountModel


class ShoppingCart(IShoppingCart):
    def calculate_total(
        self, payment_amount: PaymentAmountModel, discount_type: DiscountStrategy | str,
        strategy_map: dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy
        ) -> PaymentAmountModel:
        """
        Apply a discount type to the purchase and calculate
        the total price.
        """
        discount_strategy = get_discount_strategy(discount_type, strategy_map, default=default_discount)
        discount_value =  discount_strategy.apply_discount(payment_amount=payment_amount)
        total_price = payment_amount.amount - discount_value.amount
        
        return PaymentAmountModel(
            amount=total_price
        )