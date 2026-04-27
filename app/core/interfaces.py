from app.schemas import DiscountStrategy, BasePaymentData, PaymentAmountModel, PaymentResponse, PaymentMethods

from abc import ABC, abstractmethod
from typing import Dict

class INotificationChannel(ABC):
    """
    Interface for notification channels.
    
    Any class that implement this interface must define the methods 'notify_successful_payment' and
    notify_failed_payment
    
    Methods:
        notify_successful_payment(payment_data: BasePaymentData, payment_response: PaymentResponse) -> bool
        
            Sends a notifications to the user when the payment has been successfully
            completed.
              
        notify_failed_payment(payment_data: BasePaymentData, payment_response: PaymentResponse)

            Sends a notifications to the user when the payment has been rejected.
    """
    @abstractmethod
    async def notify_successful_payment(self, payment_data: BasePaymentData, payment_response: PaymentResponse) -> bool: ...
    
    @abstractmethod
    async def notify_failed_payment(self, payment_data: BasePaymentData, payment_response: PaymentResponse):...
    
class INotificationChannelTemplate(ABC):
    """
    Interface for notification channel templates.
    
    Any class that implement this interface must define the methods 'successful_payment_template' and
    'failed_payment_template'.
    
    Methods:
        successful_payment_template(payment_data: BasePaymentData, payment_response: PaymentResponse) -> str

            It's responsible for storing the template to send the payment confirmation message.
            
        failed_payment_template(payment_data: BasePaymentData, payment_response: PaymentResponse) -> str
        
            It's responsible for storing the template to send the payment error message.
    """
    @abstractmethod
    async def successful_payment_template(self, payment_data: BasePaymentData, payment_response: PaymentResponse) -> str: ...
    
    @abstractmethod
    async def failed_payment_template(self, payment_data: BasePaymentData, payment_response: PaymentResponse) -> str: ...

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
        calculate_total(payment_amount: PaymentAmountModel, discount_type: DiscountStrategy | str,
            strategy_map: Dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy ) -> PaymentAmountModel
        
            Apply a discount type to the purchase and calculate the total price.
    """
    @abstractmethod
    async def calculate_total(self, payment_amount: PaymentAmountModel, discount_type: DiscountStrategy | str,
        strategy_map: Dict[DiscountStrategy, IDiscountStrategy], default_discount: IDiscountStrategy 
    ) -> PaymentAmountModel: ...
    
class IPaymentGateway(ABC):
    """
    Interface for payment gateways.
    
    Any class that implement this interface must define the method 'process_payment'.
    
    Methods:
        process_payment(payment_data: BasePaymentData) -> PaymentResponse

            It's responsible for processing a payment and returning the payment details.
    """
    @abstractmethod
    async def process_payment(self, payment_data: BasePaymentData) -> PaymentResponse: ...

class IPaymentProcessor(ABC):
    """
    Interface for payment processor.
    
    Any class that implement this interface must define
    the method 'process'.
    
    Methods:
        process(payment_data: PaymentData) -> PaymentResponse
        
            processes payments with a predetermined payment method.
    """
    @abstractmethod
    async def process(self, payment_data: BasePaymentData) -> PaymentResponse: ...
    
class IPaymentMethodFactory(ABC):
    """
    This is a interface for factory of payment methods.
    
    Any class that implement this interface must defined the method 'create_payment_procesor.
    
    Methods:

        create_payment_processor(type_payment_method: PaymentMethods | str) -> IPaymentPocessor
        
            Create a payment processor based on the payment method.
    """
    @abstractmethod
    async def create_payment_processor(self, payment_method: PaymentMethods | str) -> IPaymentProcessor: ...

class INotificationService(ABC):
    """
    Interface for notification service.
    
    Any class that implement this interface must define the 'notify_all' method.
    
    Methods:
        notify_all(self, payment_response: PaymentResponse, payment_data: BasePaymentData):

            Is responsible for notifying the user through all notification channels.
        
    """
    @abstractmethod
    async def notify_all(self, payment_response: PaymentResponse, payment_data: BasePaymentData): ...