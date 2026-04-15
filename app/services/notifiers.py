from core import INotificationChannel
from schemas import PaymentData

import logging

logger = logging.getLogger(__name__)

class WhatsappChannel(INotificationChannel):
    async def notify_successful_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to the user via WhatsApp when the payment
        has been successfully completed.
        """
        # Simulating sending a message via WhatsApp.
        if payment_data.user_data.contac_info.phone_number:
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                Datos de tu compra:\n
                -----------------\n
                Valor total: {payment_data.transaction_amount}\n
                Método de pago: Pagaste con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}\n
                Id de la transacción: {payment_data.transaction_id}\n\n
                Gracias por tu compra.
                """
            )
        
        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )
        
    async def notify_rejected_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to user via WhatsApp when the payment has been
        rejected.
        """
        if payment_data.user_data.contac_info.phone_number:
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                No puedes hacer el pago con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}\n
                Pero no te preocupes, aún puedes terminar tu compra agregando recursos a tu tarjeta o cambiando de medio de pago\n\n
                
                Para más detalles contácta a tu banco.
                """
            )
        
        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )
        
    
class SmsChannel(INotificationChannel):
    async def notify_successful_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to user via SMS when the payment has
        been successfully completed.
        """
        if payment_data.user_data.contac_info.phone_number:
            # Simulating sending a message via SMS.
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                Datos de tu compra:\n
                -----------------\n
                Valor total: {payment_data.transaction_amount}\n
                Método de pago: Pagaste con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}\n
                Id de la transacción: {payment_data.transaction_id}\n\n
                Gracias por tu compra.
                """
            )
        
        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )
    
    async def notify_rejected_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to user via SMS when the payment has been rejected.
        """
        if payment_data.user_data.contac_info.phone_number:
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                No puedes hacer el pago con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}\n
                Pero no te preocupes, aún puedes terminar tu compra agregando recursos a tu tarjeta o cambiando de medio de pago\n\n
                
                Para más detalles contácta a tu banco.
                """
            )
        
        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )
    
class EmailChannel(INotificationChannel):
    async def notify_successful_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to the user via email when the payment has
        been successfully completed.
        """
        if payment_data.user_data.contac_info.email:
            message_body = f"""
            ¡Hola {payment_data.user_data.first_name}!

            Datos de tu compra:
            -------------------------
            Valor total: ${payment_data.transaction_amount}
            Método de pago: Pagaste con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}
            Id de la transacción: {payment_data.transaction_id}

            Gracias por tu compra.
            """
            # Simulating sending a message via email.
            from email.mime.text import MIMEText
            mensaje_email = MIMEText(message_body, 'plain', 'utf-8')

            mensaje_email['Subject'] = "Confirmación de tu compra"
            mensaje_email['From'] = "tienda@d1.com"
            mensaje_email['To'] = payment_data.user_data.contac_info.email
        
        logger.info(
            """
            The user could not be notified because they did not register
             a email to notify them of the purchase details.
            """
        )
        
    async def notify_rejected_payment(self, payment_data: PaymentData):
        """
        Sends a notifications to the user via email when the payment has been rejected.
        """
        if payment_data.user_data.contac_info.email:
            message_body = f"""
            ¡Hola {payment_data.user_data.first_name}!

            No puedes hacer el pago con tu tarjeta {payment_data.payment_method_id} terminada en {payment_data.last_digits_card}

            Pero no te preocupes, aún puedes terminar tu compra agregando recursos a tu tarjeta o cambiando de medio de pago
            
            Para más detalles contácta a tu banco.
            """
            # Simulating sending a message via email.
            from email.mime.text import MIMEText
            mensaje_email = MIMEText(message_body, 'plain', 'utf-8')

            mensaje_email['Subject'] = "Rechazamos tu pago"
            mensaje_email['From'] = "tienda@d1.com"
            mensaje_email['To'] = payment_data.user_data.contac_info.email
        
        logger.info(
            """
            The user could not be notified because they did not register
             a email to notify them of the purchase details.
            """
        )