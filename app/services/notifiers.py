from core import INotificationChannel
from schemas import PaymentData, PaymentResponse

from dotenv import load_dotenv
import logging
import resend
import os

_ = load_dotenv()

logger = logging.getLogger(__name__)


class WhatsappChannel(INotificationChannel):
    async def notify_successful_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
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
                Método de pago: Pagaste con tu tarjeta {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}\n
                Id de la transacción: {payment_response.transaction_id}\n\n
                Gracias por tu compra.
                """
            )

        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )
        resend.api_key = os.getenv("RESEND_API_KEY")

    async def notify_failed_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
        """
        Sends a notifications to user via WhatsApp when the payment has been
        rejected.
        """
        if payment_data.user_data.contac_info.phone_number:
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                No puedes hacer el pago con tu tarjeta {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}\n
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
    async def notify_successful_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
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
                Método de pago: Pagaste con tu tarjeta {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}\n
                Id de la transacción: {payment_response.transaction_id}\n\n
                Gracias por tu compra.
                """
            )

        logger.info(
            """
            The user could not be notified because they did not register
             a phone number to notify them of the purchase details.
            """
        )

    async def notify_failed_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
        """
        Sends a notifications to user via SMS when the payment has been rejected.
        """
        if payment_data.user_data.contac_info.phone_number:
            logger.info(
                f"""
                ¡Hola{payment_data.user_data.first_name}!\n\n
                No puedes hacer el pago con tu tarjeta {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}\n
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
    async def notify_successful_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
        """
        Sends a notifications to the user via email when the payment has
        been successfully completed.
        """
        if payment_data.user_data.contac_info.email:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": payment_data.user_data.contac_info.email,
                "subject": "Confirmación de tu compra",
                "html": self._successful_payment_template(payment_data, payment_response)
            })
            
        logger.info(
            """
            The user could not be notified because they did not register
             a email to notify them of the purchase details.
            """
        )

    async def notify_failed_payment(
        self, payment_data: PaymentData, payment_response: PaymentResponse
    ):
        """
        Sends a notifications to the user via email when the payment has been rejected.
        """
        if payment_data.user_data.contac_info.email:
            message_body = f"""
            ¡Hola {payment_data.user_data.first_name}!

            No puedes hacer el pago con tu tarjeta {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}

            Pero no te preocupes, aún puedes terminar tu compra agregando recursos a tu tarjeta o cambiando de medio de pago
            
            Para más detalles contácta a tu banco.
            """
            # Simulating sending a message via email.
            from email.mime.text import MIMEText

            mensaje_email = MIMEText(message_body, "plain", "utf-8")

            mensaje_email["Subject"] = "Rechazamos tu pago"
            mensaje_email["From"] = "tienda@d1.com"
            mensaje_email["To"] = payment_data.user_data.contac_info.email

        logger.info(
            """
            The user could not be notified because they did not register
             a email to notify them of the purchase details.
            """
        )

    def _successful_payment_template(
        self, payment_data: PaymentData, payment_response: PaymentResponse
        ) -> str:
        return f"""
            <h2>✅ Pago confirmado</h2>
            <p>Hola <b>{payment_data.user_data.first_name}</b></p>
            <table>
                <tr>
                    <td>Id de Transacción</td>                        
                    <td>{payment_response.transaction_id}</td>
                </tr>
                <tr>
                    <td>Valor Total</td>
                    <td>{payment_response.transaction_amount} {payment_response.currency}</td>
                </tr>
                <tr>
                    <td>Fecha</td>
                    <td>{payment_response.created_at}</td>
                </tr>
                <tr>
                    <td>Método de Pago</td>
                    <td>Pagaste con tu {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}</td>
                </tr>
            </table>
        """
        
    def _failed_payment_template(self, payment_data: PaymentData, payment_response: PaymentResponse
        ) -> str:
        return f"""
            <h2>❌ Rechazamos tu pago</h2>
            <p>Hola <b>{payment_data.user_data.first_name}</b></p>
            <table>
                <tr>
                    <td>Id de Transacción</td>
                    <td>{payment_response.transaction_id}
                </tr>
                <tr>
                    <td>Fecha</td>
                    <td>{payment_response.created_at}</td>
                </tr>
                <tr>
                    <td>Motivo</td>
                    <td>Saldo insuficiente en tu {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}</td>
                </tr>
            </table>
        """