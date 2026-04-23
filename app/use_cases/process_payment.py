from core import IDiscountStrategy, IShoppingCart, INotificationService, IPaymentMethodFactory
from schemas import CardPaymentData, PaymentResponse, DiscountStrategy
from typing import Dict

class ProcessPayment:
    def __init__(
            self,
            shopping_cart: IShoppingCart, 
            payment_method_factory: IPaymentMethodFactory,
            notification_service: INotificationService
            ):
        self.shopping_cart = shopping_cart
        self.payment_method_factory = payment_method_factory
        self.notification_service = notification_service
        
    async def process(self, payment_data: CardPaymentData, strategy_map: Dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy) -> PaymentResponse:
        """Create a payment processor"""
        total_amount = await self.shopping_cart.calculate_total(payment_data.transaction_amount, payment_data.discount_type, strategy_map, default_discount)
        data = CardPaymentData(
            payment_method=payment_data.payment_method,
            user_data=payment_data.user_data, 
            card_number=payment_data.card_number,
            currency=payment_data.currency,
            discount_type=payment_data.discount_type,
            transaction_amount=total_amount
        )
        
        payment_processor = await self.payment_method_factory.create_payment_processor(data.payment_method)
        payment_response = await payment_processor.process(data)
        await self.notification_service.notify_all(payment_response, data)
        
        return payment_response