from enum import Enum
from pydantic import BaseModel, Field, computed_field
from decimal import Decimal
from uuid import UUID
from datetime import datetime

from .user import UserModel

class DiscountStrategy(str, Enum):
    NODISCOUNT = "no aplica"
    CHRISTMAS = "navidad"
    FIXED = "fijo"
    BLACKFRIDAY = "black friday"

class PaymentMethods(str, Enum):
    CARD = 'tarjeta'
    PAYPAL = 'paypal'
    CRYPTO  = 'crypto'

class PaymentStatus(str, Enum):
    SUCCEDED = "succeeded"
    FAILED = "failed"
    PENDING = "pending"
    
class PaymentData(BaseModel):
    user_data : UserModel = Field(description="User's information")
    card_number : int = Field(description="Card Number")
    installments : int = Field(description="Number of installments in which the purchase will be paid", default=1)
    currency : str = Field(description="Currency code", default="COP")
    discount_type : str = Field(description="Discount type. The discount type could be 'no aplica', 'navidad', 'fijo' or 'black friday'")
    transaction_amount : Decimal = Field(
        # The amount could be
        ge=0,
        decimal_places=2,
        description="Total purchase amount"
    )
    
    class Config:
        # It allows Pydantic to automatically convert floats or strings to Decimal.
        json_encoders = {Decimal: str}
         
class PaymentAmountModel(BaseModel):
    transaction_amount : Decimal = Field(
        # The amount could be
        ge=0,
        decimal_places=2,
        description="Total payment amount"
    )

class PaymentResponse(BaseModel):
    currency : str = Field(description="Currency code", default="COP")
    payment_method_id : str = Field(description="Processing network that was used for payment")
    transaction_id : UUID = Field(description="Trasaction id")
    payment_status : str = Field(description="Payment status")
    created_at : datetime = Field(description="Transaction timestamp")
    message : str | None = Field(description="Message with payment information")
    transaction_amount : Decimal = Field(
        ge=0,
        decimal_places=2,
        description="Amount charged"
    )
    
    @computed_field(description="Last four digits of the card")
    @property
    def last_digits_card(self):
        card_number_str = str(PaymentData.card_number)
        last_digits = card_number_str[:4]
        return int(last_digits)