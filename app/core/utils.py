from .constants import PROCESSING_NETWORK_RULES
from .interfaces import INotificationChannel
from .strategies import get_notification_method
from schemas import PaymentResponse, PaymentAmountModel

from collections import deque
from typing import List, Type
import logging

logger = logging.getLogger(__name__)

async def luhn_algorit(card_number: int) -> bool:
    """
    Valid if the card number is mathematically correct.
    """
    position = 1
    total_sum = 0
    
    while card_number > 0:
        last_digit = card_number % 10
        
        if position % 2 == 0:
            new_value = last_digit * 2
        
            if new_value > 9:
                new_value -= 9
            total_sum += new_value
        else:
            total_sum += last_digit
            
        card_number = card_number // 10
        position += 1
        
    if total_sum % 10 == 0:
        return True
    
    return False

async def validate_card_length(processing_network: str, card_number: int) -> bool:
    """
    Valid if the card number length is valid, depending
    on your processing network.
    """
    for rule in PROCESSING_NETWORK_RULES:
        if rule['name'] == processing_network:
            return len(str(card_number)) in rule['lengths']
    
    return False

async def to_stripe_amount(payment_amount: PaymentAmountModel) -> int:
    """
    It's responsible for transferring the payment amount to Stripe in the requested format.
    """
    return int(payment_amount.transaction_amount * 100)
        
async def dequeue(
        notifiers_queue: deque, 
        payment_response: PaymentResponse
        ) -> List[Type[INotificationChannel] | None]:
        # A list is compiled of the channels where the notifiers failed
        notifiers_failed = []
        
        while notifiers_queue:
            notifier, attempts = notifiers_queue.popleft()
            notification_method = await get_notification_method(payment_response, notifier)
            
            if not notification_method:
                logger.critical("No notification method was found for the notification channels")
                raise RuntimeError("No notification method was found for the notification channels")
            
            if await notifier.notification_method(payment_response):
                logger.info(f"Notification success with {notifier}")
            else:
                new_attempts = attempts + 1
                if new_attempts < 3:
                    notifiers_queue.append((notifier, new_attempts))
                else:
                    notifiers_failed.append(notifier)
        
        return notifiers_failed