from schemas import PaymentMethods, DiscountStrategy
from core import IDiscountStrategy
from .strategy import PROCESSING_NETWORK_RULES

from enum import Enum
from typing import Dict, Type

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
            raise ValueError(f"The payment method of type {type_payment_method} not found")
    else:
        return type_payment_method
   
def get_discount_strategy(
    discount_type: DiscountStrategy | str,
    strategy_map: Dict[Enum, Type[IDiscountStrategy]],
    default: Type[IDiscountStrategy] | None = None
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
        raise RuntimeError("Critical error: No default strategy was found on the map")
    
    return strategy_class()

def get_processing_network(card_number: int) -> str | None:
    """
    Search for a processing network based on the card number.
    """
    s_card = str(card_number)
    iin_code = int(s_card[:4])
    for rule in PROCESSING_NETWORK_RULES:
        if s_card.startswith(rule['prefixes']):
            return rule['name']

        for start, end in rule['ranges']:
            if start <= iin_code <= end:
                return rule['name']
    return None