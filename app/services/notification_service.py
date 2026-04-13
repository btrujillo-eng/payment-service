from core import NOTIFICATIONS_QUEUE, dequeue
from schemas import PurchaseDetailsModel

from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """
    This is a notification service.
    
    It's responsible for sending notification with information about the details of the purchase.
    """
    async def notify_all(self, purchase_details: PurchaseDetailsModel):
        notifiers_failed = await dequeue(NOTIFICATIONS_QUEUE, purchase_details)
        if notifiers_failed:
            logger.error(f"Critical failure: The notification service is not responding | Transaction id: {purchase_details.transaction_id}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio temporalmente inestable. Intente nuevamente mas tarde"
            )
        logger.info(
            f"""
                The user {purchase_details.user_data.first_name} {purchase_details.user_data.middle_name} was sucessfully notified of id: {purchase_details.transaction_id}
            """
        )