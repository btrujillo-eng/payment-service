from app.core.interfaces import INotificationChannel
from app.core.strategies import get_notification_method
from app.schemas import PaymentResponse, BasePaymentData

from collections import deque
from typing import List, Type
import logging

logger = logging.getLogger(__name__)
    
async def dequeue(
        notifiers_queue: deque, 
        payment_response: PaymentResponse,
        payment_data: BasePaymentData
    ) -> List[Type[INotificationChannel] | None]:
    """
    It is responsible for emptying the notification channel queue
    """
    # A list is compiled of the channels where the notifiers failed
    notifiers_failed = []
        
    while notifiers_queue:
        notifier, attempts = notifiers_queue.popleft()
        notification_method = await get_notification_method(payment_response, notifier)
            
        if not notification_method:
            logger.critical("No notification method was found for the notification channels")
            raise RuntimeError("No notification method was found for the notification channels")
            
        if await notification_method(payment_data, payment_response):
            logger.info(f"Notification success with {notifier}")
        else:
            new_attempts = attempts + 1
            if new_attempts < 3:
                notifiers_queue.append((notifier, new_attempts))
            else:
                notifiers_failed.append(notifier)
        
    return notifiers_failed