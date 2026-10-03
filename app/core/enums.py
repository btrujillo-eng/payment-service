from enum import Enum


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
    
class TypeCurrency(str, Enum):
    USD = 'usd'
    COP = 'cop'