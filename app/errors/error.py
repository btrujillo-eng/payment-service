class NotificationServiceError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        
class PaymentProcessorError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        
class CardPaymentProcessorError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        
class StripeGatewayError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
            
class CardPaymentMethodError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message
        
class CVVCardError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message
        
class NotificationTemplateError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message