from enum import Enum
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Literal
from uuid import UUID

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
  
class AmountPurchasedModel(BaseModel):
    amount : Decimal = Field(
        # The amount coul be 0 
        ge=0,
        decimal_places=2,
        description="Total amount with decimal precision"
        )
    
    class Config:
        # It allows Pydantic to automatically convert floats or strings to Decimal.
        json_encoders = {Decimal: str}

# To configure the payment status soon.
PaymentStatus = Literal['succeded', 'rejected']
      
class PaymentData(BaseModel):
    user_data : UserModel = Field(description="User's information")
    transaction_amount : Decimal = Field(
        ge=0,
        decimal_places=2,
        description="Total purchase amount"
        )
    payment_method_id : str = Field(description="Processing network that was used for payment")
    transaction_id : UUID | None = Field(description="Trasaction id")
    installments : int | None = Field(description="Number of installments in which the purchase will be paid")
    payment_status : PaymentStatus = Field(description="Payment status. The status could be 'succeded' or 'rejected'")
    last_digits_card : int = Field(description="Last four digits of the card used for payment")