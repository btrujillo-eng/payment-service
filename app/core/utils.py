from .strategy import PROCESSING_NETWORK_RULES
from .interfaces import INotificationChannel
from schemas import PaymentData

from collections import deque
from typing import List, Type

def luhn_algorit(card_number: int) -> bool:
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

def validate_card_length(processing_network: str, card_number: int) -> bool:
    """
    Valid if the card number length is valid, depending
    on your processing network.
    """
    for rule in PROCESSING_NETWORK_RULES:
        if rule['name'] == processing_network:
            return len(str(card_number)) in rule['lengths']
    
    return False
        
async def dequeue(
        notifiers_queue: deque, 
        purchase_details: PaymentData
        ) -> List[Type[INotificationChannel] | None]:
        # A list is compiled of the channels where the notifiers failed
        notifiers_failed = []
        while notifiers_queue:
            notifier, attempts = notifiers_queue.popleft()
            if await notifier.notify(purchase_details):
                print(f"Notification success with {notifier}")
            else:
                new_attempts = attempts + 1
                if new_attempts < 3:
                    notifiers_queue.append((notifier, new_attempts))
                else:
                    notifiers_failed.append(notifier)
        
        return notifiers_failed
    