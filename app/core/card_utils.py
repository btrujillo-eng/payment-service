from .constants import PROCESSING_NETWORK_RULES

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