from abc import ABC, abstractmethod
from schemas import DiscountStrategy, AmountPurchasedModel, PaymentData

class INotificationChannel(ABC):
    """
    Interface for notification channels.
    
    Any class that implement this interface must define the
    method 'notify'.
    
    Methods:
        notify(purchase_details: PurchaseDetails) -> bool
        
            Sends a notifications to the user.
    """
    @abstractmethod
    async def notify(self, purchase_details: PaymentData) -> bool: ...

class ICardValidator(ABC):
    """
    Interface for validating cards.
    
    Any class that implement this interface must define the
    method 'validate'.
    
    Methods:
        validate(card_number: int) -> bool
        
            Valid if a card is valid based on your number.
    """
    @abstractmethod
    def validate(self, card_number: int) -> bool:...
    
class IDiscountStrategy(ABC):
    """
    Interface for applying discounts to purchases.
    
    Any class that implement this interface must define the
    method 'apply_discount'.
    
    IMPORTANT!:
        Implementations of this interface should only return the 
        discount value.
    
    Methods:
        apply_discount(amount_purchased: AmountModel) -> AmountModel
        
            Returns the discount value.
    """
    @abstractmethod
    def apply_discount(self, amount_purchased: AmountPurchasedModel) -> AmountPurchasedModel: ...
          
class IShoppingCart(ABC):
    """
    Interface for a shopping cart.
    
    Any class that implement this interface must define the
    method 'calculate_total'.
    
    Methods:
        calculate_total(amount_purchased: AmountModel, discount_type: DiscountStrategy | str) -> AmountModel
        
            Apply a discount type to the purchase and calculate
            the total price.
    """
    @abstractmethod
    def calculate_total(
        self,
        amount_purchased: AmountPurchasedModel,
        discount_type: DiscountStrategy | str
    ) -> AmountPurchasedModel: ...

class IPaymentPocessor(ABC):
    """
    Interface for payment processor.
    
    Any class that implement this interface must define
    the method 'process'.
    
    Methods:
        process(
            self, payment_method: str, discount_type: DiscountStrategy | str,
            amount_purchased: AmountPurchasedModel
            ) -> str
        
            processes payments with a predetermined payment method.
    """
    @abstractmethod
    def process(
        self, payment_method: str, discount_type: DiscountStrategy | str,
        amount_purchased: AmountPurchasedModel
        ) -> str: ...