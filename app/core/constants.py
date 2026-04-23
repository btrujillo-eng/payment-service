from app.schemas import PaymentStatus

from typing import Dict, List, Any

PROCESSING_NETWORK_RULES: List[Dict[str, Any]] = [
    {"name": "Visa", "prefixes": ("4",), "ranges": [], "lengths": [13, 16]},
    {"name": "American Express", "prefixes": ('34', '37'), "ranges": [], "lengths": [15]},
    {"name": "Mastercard", "prefixes": ("51", "52", "53", "54", "55",), "ranges": [(2221, 2720)], "lengths": [16]},
    {"name": "Discover", "prefixes": (6011,), "ranges": [(644, 650)], "lengths": [16]}
]

NOTIFICATION_METHOD: Dict[PaymentStatus, str] = {
    PaymentStatus.FAILED: "notify_rejected_payment",
    PaymentStatus.SUCCEDED: "notify_successful_payment"
}