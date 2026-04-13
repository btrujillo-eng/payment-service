from schemas import PaymentMethods
from core import IPaymentPocessor, get_payment_method, INotificationChannel
from core.strategy import NOTIFICATIONS_QUEUE

from collections import deque
from typing import Type, Tuple

class PaymentMethodFactory:
    """
    This class is a factory of payment methods.
    
    Any class that implement this factory must defined
    the method 'create_payment_procesor.
    
    Methods:

        create_payment_processor(type_payment_method: PaymentMethods | str) -> IPaymentPocessor
        
            Create a payment processor based on the payment method.
    """
    def __init__(
            self,
            card_method: Type[IPaymentPocessor],
            paypal_method: Type[IPaymentPocessor],
            cripto_method: Type[IPaymentPocessor]
            ):
        self.payment_methods = {
            PaymentMethods.CARD: card_method,
            PaymentMethods.PAYPAL: paypal_method,
            PaymentMethods.CRYPTO: cripto_method 
        }
        
        def create_payment_processor(payment_method: PaymentMethods | str) -> IPaymentPocessor:
            """
            Create a payment processor based on the payment method.
            """
            payment_type = get_payment_method(payment_method)
            processor_class = self.payment_methods.get(payment_type)
            
            if not processor_class:
                raise  RuntimeError(
                    f"The payment method '{payment_type}' is soport for the sistem, "
                    "but a processor has not been implementation in the factory"
                )
            return processor_class()

# class NotificationChannelFactory:
#     """
#     This class is a factory notifications channel.
    
#     Any class that implement this factory must define the
#     method 'create_notification_channel'.
    
#     Methods:
#         create_notification_channel(notifiers: Tuple[Type[INotificationChannel], int])
#     """
#     def __init__(self):
#         self.notifiers_queue: deque[Tuple[Type[INotificationChannel], int]] = deque()
        
#     def create_notification_channel(
#         self,
#         notifiers: Tuple[Type[INotificationChannel], int]
#         ) -> deque[Tuple[Type[INotificationChannel], int]]:
#         """
#         Create a queue with the avaible notifiers.
#         """
#         [self.notifiers_queue.append(notifier) for notifier in notifiers]
#         return self.notifiers_queue