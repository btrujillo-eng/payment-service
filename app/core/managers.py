from schemas import PaymentMethods, DiscountStrategy, PaymentData, PaymentStatus
from core import IDiscountStrategy, INotificationChannel
from .strategy import PROCESSING_NETWORK_RULES, NOTIFICATION_METHOD

from typing import Dict, cast
import logging

logger = logging.getLogger(__name__)

def get_payment_method(type_payment_method: PaymentMethods | str) -> PaymentMethods:
    """
    It searches for a payment method and returns it depending on the type payment method.
    
    The type payment method could be 'tarjeta', 'paypal', or 'crypto'.
    """
    if isinstance(type_payment_method, str):
        try:
            enum_method = PaymentMethods(type_payment_method.strip().lower())
            return enum_method
        except ValueError:
            logger.error(f"The payment method of type {type_payment_method} not found")
            raise ValueError(f"The payment method of type {type_payment_method} not found")
    else:
        return type_payment_method
   
def get_discount_strategy(
        discount_type: DiscountStrategy | str,
        strategy_map: Dict[DiscountStrategy, IDiscountStrategy],
        default: IDiscountStrategy | None = None
    ) -> IDiscountStrategy:
    """
    It searches a strategic discount and returns it dependig on the discount type.
    
    The discount type could be 'no aplica', 'navidad', 'fijo' or 'black friday'.
    """
    if isinstance(discount_type, str):
        try:
            discount_type = DiscountStrategy(discount_type.strip().lower())
        except ValueError:
            discount_type = DiscountStrategy.NODISCOUNT
            
    default_class = default
    strategy_class = strategy_map.get(discount_type, default_class)
    if not strategy_class:
        logger.critical("No default strategy was found on the map")
        raise RuntimeError("Critical error: No default strategy was found on the map")
    
    return strategy_class

def get_processing_network(card_number: int) -> str | None:
    """
    Search for a processing network based on the card number.
    """
    s_card = str(card_number)
    iin_code = int(s_card[:4])
    for network in PROCESSING_NETWORK_RULES:
        if s_card.startswith(network['prefixes']):
            return network['name']

        for start, end in network['ranges']:
            if start <= iin_code <= end:
                return network['name']
            
    return None

def get_notification_method(payment_data: PaymentData, channel_instance: INotificationChannel):
    status = cast(PaymentStatus, payment_data.payment_status)
    method_name = NOTIFICATION_METHOD.get(status)
    if not method_name:
        method_name = "notify_rejected_payment"
    
    # getattr getattrs is used to dynamically search for a method in its object or instance using its name in str.
    method = getattr(channel_instance, method_name, None)
    return method