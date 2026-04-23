from errors.error import NotificationServiceError
from schemas import PaymentResponse, BasePaymentData
from core import INotificationChannel, INotificationService, dequeue

from collections import deque
from typing import List
import logging

logger = logging.getLogger(__name__)

class NotificationService(INotificationService):
    """
    This is a notification service.
    
    It's responsible for sending notification with information regarding payment details to user.
    Any class that implement this service can define the 'notify_all' method
    """
    def __init__(self, list_channels: List[INotificationChannel]):
        self.list_channels = list_channels
        
    async def notify_all(self, payment_response: PaymentResponse, payment_data: BasePaymentData):
        """
        Is responsible for notifying the user through all notification channels.
        """
        queue = deque([(channel, 0) for channel in self.list_channels])
        notifiers_failed = await dequeue(queue, payment_response, payment_data)
        if notifiers_failed:
            logger.error(f"Critical failure: The notification service is not responding | Transaction id: {payment_response.transaction_id}")
            raise NotificationServiceError("Critical failure: notification service unavailable")
        
        logger.info(
            f"""
                The user {payment_data.user_data.first_name} {payment_data.user_data.first_surname} was successfully notified of id: {payment_response.transaction_id}
            """
        )