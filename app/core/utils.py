from .strategy import PROCESSING_NETWORK_RULES
from schemas import PurchaseDetailsModel

from collections import deque

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
        
def dequeue(notifiers_queue: deque, purchase_details: PurchaseDetailsModel):
        while notifiers_queue:
            notifier, attempts = notifiers_queue.popleft()
            if not notifier.notify(purchase_details):
                print(f"Notificación exitosa con {notifier}")
            else:
                new_attemps = attempts + 1
                print(f"Fallo. Reintentando {new_attemps}")
                
                if attempts + 1 < 3:
                    notifiers_queue.append((notifier, attempts + 1))
                else:
                    # Simulating writing to technical support.
                    print("Sending channels notiifers failed to tecnhical support")
                    notifiers_failed = []
                    notifiers_failed.append(notifier)
                    continue
        return notifiers_failed
        
#print(luhn_algorit(4532015112830366))
    