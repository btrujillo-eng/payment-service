from services.discounts import NoDiscount, ChristmasDiscount, FixedDiscount, BlackFridayDiscount
from services.notifiers import EmailChannel, WhatsappChannel, SmsChannel
from schemas import DiscountStrategy
from core import IDiscountStrategy, INotificationChannel

from typing import Dict, List, Any, Type, Tuple
from collections import deque

STRATEGY_MAP: Dict[DiscountStrategy, IDiscountStrategy] = {
        DiscountStrategy.NODISCOUNT: NoDiscount,
        DiscountStrategy.CHRISTMAS: ChristmasDiscount,
        DiscountStrategy.FIXED: FixedDiscount,
        DiscountStrategy.BLACKFRIDAY: BlackFridayDiscount
    }

PROCESSING_NETWORK_RULES: List[Dict[str, Any]] = [
    {"name": "Visa", "prefixes": ("4",), "ranges": [], "lengths": [13, 16]},
    {"name": "American Express", "prefixes": ('34', '37'), "ranges": [], "lengths": [15]},
    {"name": "Mastercard", "prefixes": ("51", "52", "53", "54", "55",), "ranges": [(2221, 2720)], "lengths": [16]},
    {"name": "Discover", "prefixes": (6011,), "ranges": [(644, 650)], "lengths": [16]}
]

NOTIFICATIONS_QUEUE: Tuple[Type[INotificationChannel], int] = (
    (EmailChannel, 0),
    (WhatsappChannel, 0),
    (SmsChannel, 0)
)