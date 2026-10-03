from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    SecretStr,
    model_validator,
)

from app.core.card_utils import validate_cvv_card
from app.core.card_validator import CardValidator
from app.core.enums import PaymentMethods, TypeCurrency
from app.errors import CVVCardError
from app.schemas.user import BaseUserData
    
TransactionAmount = Annotated[Decimal, Field(gt=0, decimal_places=2)]

Currency = Annotated[TypeCurrency, Field(description="Currency code")]

CardNumber = Annotated[SecretStr, Field(description="Card Number"), BeforeValidator(CardValidator())]

Message = Annotated[str, Field(description="Message with payment information")]

class CashPaymentData(BaseModel):
    method : Literal[PaymentMethods.CASH]

class CardPaymentData(BaseModel):
    method : Literal[PaymentMethods.CARD]
    card_number : CardNumber
    cvv: SecretStr = Field(min_length=3, max_length=4, description="Card Verification Value")
    
    @model_validator(mode="after")
    def validate_cvv(self) -> Self:
        if not validate_cvv_card(self.cvv.get_secret_value(), self.card_number.get_secret_value()):
            raise CVVCardError("The CVV card is invalid")
        
        return self
               
PaymentMethod = Annotated[
    CashPaymentData | CardPaymentData, 
    Field(discriminator="method", description="Specific information about the payment method")]

class BasePaymentData(BaseModel):
    user_data : BaseUserData = Field(description="User's information")
    currency : Currency = TypeCurrency.COP
    discount_type : str = Field(description="Discount type. The discount type could be 'no aplica', 'navidad', 'fijo' or 'black friday'")
    transaction_amount : Annotated[TransactionAmount, Field(description="Total payment amount")]
    payment_method: PaymentMethod
    
class CardPaymentResponse(BaseModel):
    method: Literal[PaymentMethods.CARD]
    processing_network: str = Field(description="Card processing network used for payment")
    last_digits: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$",  description="Last four digits of the card")
    
class CashPaymentResponse(BaseModel):
    method : Literal[PaymentMethods.CASH]
    
PaymentMethodResponse = Annotated[
    CardPaymentResponse | CashPaymentResponse, 
    Field(discriminator="method", description="Payment method used")
]
    
class PaymentResponse(BaseModel):
    currency : Currency = TypeCurrency.COP
    transaction_amount : Annotated[ TransactionAmount, Field(description="Charged amount")]
    transaction_id : str = Field(description="Trasaction id")
    payment_status : str = Field(description="Payment status")
    message : Message | None = None
    created_at : datetime = Field(description="Transaction timestamp")
    payment_method : PaymentMethodResponse