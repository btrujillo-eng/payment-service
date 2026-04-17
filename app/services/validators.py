from core import ICardValidator, get_processing_network, validate_card_length, luhn_algorit

class CardValidator(ICardValidator):
    async def validate(self, card_number: int) -> bool:
        """
        Valid if a card is valid based on his number.
        
        For the validation of the card this method is based
        on three steps.
        
        1. Search for a processing network based on his IIN Prefixe.
        
        2. Valid if the card number length is valid, depending on his processing network.
        
        3. Used the luhn algorit for calculate if the card number is mathematically correct.
        
        if the card is valid returns True, otherwise returns False.
        """
        processing_network = await get_processing_network(card_number)
        if not processing_network:
            return False
        
        length_valid = await validate_card_length(processing_network, card_number)
        if not length_valid:
            return False
        
        card_valid = await luhn_algorit(card_number)
        if not card_valid:
            return False
        
        return True