import os

from dotenv import load_dotenv

from app.core import IDiscountStrategy, INotificationChannel, PaymentMethodFactory
from app.infrastructure import StripeGateway
from app.notifications import (
    EmailChannel,
    EmailChannelTemplate,
    NotificationService,
)
from app.schemas import DiscountStrategy
from app.services import (
    BlackFridayDiscount,
    CardPaymentProcessor,
    CardValidator,
    ChristmasDiscount,
    FixedDiscount,
    NoDiscount,
    ShoppingCart,
)
from app.use_cases import ProcessPayment

_ = load_dotenv()

def get_stripe_gateway() -> StripeGateway:
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise ValueError("API key not found")
    return StripeGateway(api_key)

def get_card_validator() -> CardValidator:
    return CardValidator()

def get_card_processor() -> CardPaymentProcessor:
    return CardPaymentProcessor(get_card_validator(), get_stripe_gateway())

def get_payment_method_factory() -> PaymentMethodFactory:
     # TODO: implement CashPaymentProcessor
    return PaymentMethodFactory(get_card_processor(), get_card_processor())

def get_shopping_cart() -> ShoppingCart:
    return ShoppingCart()

def get_notification_channels() -> list[INotificationChannel]:
    #phone_template = PhoneChannelTemplate()
    email_template = EmailChannelTemplate()
    return [
        EmailChannel(email_template),
        #SmsChannel(phone_template),
        #WhatsappChannel(phone_template)
    ]

def get_notification_service() -> NotificationService:
    return NotificationService(get_notification_channels())

def get_process_payment() -> ProcessPayment:
    return ProcessPayment(get_shopping_cart(), get_payment_method_factory(), get_notification_service())

def get_strategy_map() -> dict[DiscountStrategy, IDiscountStrategy]:
    return {
        DiscountStrategy.NODISCOUNT: NoDiscount(),
        DiscountStrategy.CHRISTMAS: ChristmasDiscount(),
        DiscountStrategy.FIXED: FixedDiscount(),
        DiscountStrategy.BLACKFRIDAY: BlackFridayDiscount()
    }

def get_default_discount() -> IDiscountStrategy:
    return NoDiscount()
