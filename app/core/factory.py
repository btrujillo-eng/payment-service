from core import IPaymentPocessor, get_payment_method
from schemas import PaymentMethods

from typing import Type
import logging

logger = logging.getLogger(__name__)

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
                logger.warning(
                    f"The payment method '{payment_type}' is soport for the sistem, "
                    "but a processor has not been implementation in the factory"
                )
                raise  RuntimeError(
                    f"The payment method '{payment_type}' is soport for the sistem, "
                    "but a processor has not been implementation in the factory"
                )
            return processor_class()