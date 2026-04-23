class NotificationServiceError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
        
class PaymentProcessorError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        
class CardPaymentProcessorError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message