from app.core import (
    IDiscountStrategy,
    INotificationService,
    IPaymentMethodFactory,
    IShoppingCart,
)
from app.schemas import CardPaymentData, DiscountStrategy, PaymentResponse


class ProcessPaymentUseCase:
    def __init__(
            self,
            shopping_cart: IShoppingCart,
            payment_method_factory: IPaymentMethodFactory,
            notification_service: INotificationService
            ):
        self.shopping_cart = shopping_cart
        self.payment_method_factory = payment_method_factory
        self.notification_service = notification_service

    def process(self, payment_data: CardPaymentData, strategy_map: dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy) -> PaymentResponse:
        """Create a payment processor"""
        total_amount = self.shopping_cart.calculate_total(payment_data.transaction_amount, payment_data.discount_type, strategy_map, default_discount)
        data = CardPaymentData(
            payment_method=payment_data.payment_method,
            user_data=payment_data.user_data, 
            card_number=payment_data.card_number,
            currency=payment_data.currency,
            discount_type=payment_data.discount_type,
            transaction_amount=total_amount
        )
        payment_processor =self.payment_method_factory.create_payment_processor(data.payment_method)
        payment_response = payment_processor.process(data)
        self.notification_service.notify_all(payment_response, data)
        return payment_response