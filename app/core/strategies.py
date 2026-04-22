from schemas import PaymentMethods, DiscountStrategy, PaymentResponse, PaymentStatus
from .interfaces import IDiscountStrategy, INotificationChannel
from .constants import PROCESSING_NETWORK_RULES, NOTIFICATION_METHOD

from typing import Dict
import logging

logger = logging.getLogger(__name__)

async def get_payment_method(type_payment_method: PaymentMethods | str) -> PaymentMethods:
    """
    It searches for a payment method and returns it depending on the type payment method.
    
    The type payment method could be 'tarjeta', 'paypal', or 'crypto'.
    """
    if isinstance(type_payment_method, str):
        try:
            type_payment_method = PaymentMethods(type_payment_method.strip().lower())
        except ValueError:
            logger.error(f"The payment method of type {type_payment_method} not found")
            raise ValueError(f"The payment method of type {type_payment_method} not found")
    
    return type_payment_method
   
async def get_discount_strategy(
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

async def get_processing_network(card_number: int) -> str | None:
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

async def get_payment_status(payment_status: PaymentStatus | str, default: PaymentStatus) -> PaymentStatus:
    """
    It is responsible for finding the payment status.
    """
    if isinstance(payment_status, str):
        try:
            payment_status = PaymentStatus(payment_status.strip().lower())
        except ValueError:
            return default
            
    return payment_status
    
async def get_notification_method(payment_response: PaymentResponse, channel_instance: INotificationChannel):
    """
    It is responsible for finding the notification method.
    """
    status = await get_payment_status(payment_response.payment_status, PaymentStatus.FAILED)
    method_name = NOTIFICATION_METHOD.get(status)
    if not method_name:
        method_name = "notify_rejected_payment"
    
    # getattr is used to dynamically search for a method in its object or instance using its name in str.
    method = getattr(channel_instance, method_name, None)
    return method