from .notifiers import EmailChannel, WhatsappChannel, SmsChannel
from schemas import PaymentData
from core import dequeue

from fastapi import HTTPException, status
from collections import deque
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """
    This is a notification service.
    
    It's responsible for sending notification with information about the details of the purchase.
    """
    def __init__(
            self, 
            email_channel: EmailChannel,
            whatsapp_channel: WhatsappChannel,
            sms_channel: SmsChannel
        ):
        self.email_channel = email_channel
        self.whatsapp_channel = whatsapp_channel
        self.sms_channel = sms_channel  
    
    async def notify_all(self, purchase_details: PaymentData):
        queue = deque([(self.email_channel, 0), (self.whatsapp_channel, 0), (self.sms_channel, 0)])
        notifiers_failed = await dequeue(queue, purchase_details)
        if notifiers_failed:
            logger.error(f"Critical failure: The notification service is not responding | Transaction id: {purchase_details.transaction_id}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio temporalmente inestable. Intente nuevamente mas tarde"
            )
        logger.info(
            f"""
                The user {purchase_details.user_data.first_name} {purchase_details.user_data.first_surname} was successfully notified of id: {purchase_details.transaction_id}
            """
        )