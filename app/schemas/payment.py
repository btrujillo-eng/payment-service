from enum import Enum
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Literal

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
        
class PurchaseDetailsModel(BaseModel):
    user_data : UserModel = Field(description="User's information")
    amount_purchase : Decimal = Field(
        ge=0,
        decimal_places=2,
        description="Total purchase amount"
        )
    payment_method : str

# To configure the purchase status soon.
PurchaseStatus = Literal['succeded', 'rejected']