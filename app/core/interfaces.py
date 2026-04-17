from schemas import DiscountStrategy, PaymentData, PaymentAmountModel, PaymentResponse

from abc import ABC, abstractmethod

class INotificationChannel(ABC):
    """
    Interface for notification channels.
    
    Any class that implement this interface must define the
    method 'notify'.
    
    Methods:
        notify_successful_payment(payment_data: PaymentData, payment_response: PaymentResponse)
        
            Sends a notifications to the user when the payment has been successfully
            completed.
              
        notify_rejected_payment(payment_data: PaymentData, payment_response: PaymentResponse)

            Sends a notifications to the user when the payment has been rejected.
    """
    @abstractmethod
    async def notify_successful_payment(self, payment_data: PaymentData, payment_response: PaymentResponse): ...
    
    @abstractmethod
    async def notify_failed_payment(self, payment_data: PaymentData, payment_response: PaymentResponse):...
    
class INotificationChannelTemplate(ABC):
    
    @abstractmethod

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
    async def validate(self, card_number: int) -> bool:...
    
class IDiscountStrategy(ABC):
    """
    Interface for applying discounts to purchases.
    
    Any class that implement this interface must define the
    method 'apply_discount'.
    
    IMPORTANT!:
        Implementations of this interface should only return the 
        discount value.
    
    Methods:
        apply_discount(payment_amount: AmountModel) -> AmountModel
        
            Returns the discount value.
    """
    @abstractmethod
    async def apply_discount(self, payment_amount: PaymentAmountModel) -> PaymentAmountModel: ...
          
class IShoppingCart(ABC):
    """
    Interface for a shopping cart.
    
    Any class that implement this interface must define the method 'calculate_total'.
    
    Methods:
        calculate_total(payment_amount: AmountModel, discount_type: DiscountStrategy | str) -> AmountModel
        
            Apply a discount type to the purchase and calculate
            the total price.
    """
    @abstractmethod
    def calculate_total(
        self,
        payment_amount: PaymentAmountModel,
        discount_type: DiscountStrategy | str
    ) -> PaymentAmountModel: ...
    
class IPaymentGateway(ABC):
    """
    Interface for payment gateways.
    
    Any class that implement this interface must define the method 'process_payment'.
    
    Methods:
        process_payment(payment_data: PaymentData) -> PaymentResponse

            It's responsible for processing a payment and returning the payment details.
    """
    @abstractmethod
    async def process_payment(self, payment_data: PaymentData) -> PaymentResponse: ...

class IPaymentProcessor(ABC):
    """
    Interface for payment processor.
    
    Any class that implement this interface must define
    the method 'process'.
    
    Methods:
        process(
            self, payment_method: str, discount_type: DiscountStrategy | str,
            payment_amount: AmountPurchasedModel
            ) -> str
        
            processes payments with a predetermined payment method.
    """
    @abstractmethod
    async def process(
        self, payment_method: str, discount_type: DiscountStrategy | str,
        payment_amount: PaymentAmountModel
        ) -> str: ...