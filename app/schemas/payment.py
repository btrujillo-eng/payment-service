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
    CASH = 'efectivo'

class PaymentStatus(str, Enum):
    SUCCEDED = "succeeded"
    FAILED = "failed"
    PENDING = "pending"
         
class PaymentAmountModel(BaseModel):
    transaction_amount : Decimal = Field(
        # The amount could be
        ge=0,
        decimal_places=2,
        description="Total payment amount"
    )
     
class BasePaymentData(BaseModel):
    user_data : UserModel = Field(description="User's information")
    payment_method: PaymentMethods = Field(description="Payment method. Could be 'tarjeta' o 'efectivo'")
    currency : str = Field(description="Currency code", default="COP")
    discount_type : str = Field(description="Discount type. The discount type could be 'no aplica', 'navidad', 'fijo' or 'black friday'")
    transaction_amount : PaymentAmountModel = Field(description="Total purchase amount")
    
    class Config:
        # It allows Pydantic to automatically convert floats or strings to Decimal.
        json_encoders = {Decimal: str}
        
class CardPaymentData(BasePaymentData):
    card_number : int = Field(description="Card Number")

class PaymentResponse(BaseModel):
    currency : str = Field(description="Currency code", default="COP")
    payment_method_id : str = Field(description="Processing network that was used for payment")
    transaction_id : UUID = Field(description="Trasaction id")
    payment_status : str = Field(description="Payment status")
    created_at : datetime = Field(description="Transaction timestamp")
    message : str | None = Field(description="Message with payment information")
    card_number: int
    transaction_amount : PaymentAmountModel = Field(description="Amount charged")
    
    @computed_field(description="Last four digits of the card")
    @property
    def last_digits_card(self):
        return int(str(self.card_number)[-4:])