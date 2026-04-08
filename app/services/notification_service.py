from core import NotificationChannelFactory, NOTIFICATIONS_QUEUE

class NotificationService:
    def __init__(
            self,
            notification_factory: NotificationChannelFactory
            ):
        self.notification_factory = notification_factory
        
    async def notify_all(self):
        notifications_queue = self.notification_factory.create_notification_channel(NOTIFICATIONS_QUEUE)
        while self.notification_factory:
            await notifications_queue()