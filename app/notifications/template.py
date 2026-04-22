from schemas import PaymentData, PaymentResponse
from core import INotificationChannelTemplate

class EmailChannelTemplate(INotificationChannelTemplate):
    """
    This is the Email Channel Template.
    
    It's responsible for storing the templates for email notifications to the user regarding payment details. Any class that
    implements this template can define the 'successful_payment_template' and 'failed_payment_template' methods.
    """
    async def successful_payment_template(self, payment_data: PaymentData, payment_response: PaymentResponse) -> str:
        """
        It's responsible for store the template to send the payment confirmation message by email.
        """
        return f"""
            <h2>Pago confirmado 😎</h2>
            <p>¡Hola <b>{payment_data.user_data.first_name}!</b></p>
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
                <p><strong>¡Gracias por tu compra 🙋‍♂️!</strong></p>
            </table>
        """
        
    async def failed_payment_template(self, payment_data: PaymentData, payment_response: PaymentResponse) -> str:
        """
        It's responsible for store the template to send the payment error message by email.
        """  
        return f"""
            <h2>Tu pago fue rechazado 🥲</h2>
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
            <p><strong>¡Por favor intenta nuevamente 😉!</strong></p>
        """
        
class PhoneChannelTemplate(INotificationChannelTemplate):
    """
    This is the Phone Channel Template.
    
    It's responsible for storing the templates for SMS and WhatsApp notifications to the user regarding payment details. Any 
    class that implements this template can define the 'successful_payment_template' and 'failed_payment_template'  methods.
    """
    async def successful_payment_template(self, payment_data: PaymentData, payment_response: PaymentResponse) -> str:
        return f"""
            **Pago confirmado 😎**\n\n
            ¡Hola {payment_data.user_data.first_name}!\n
            
            Datos de tu compra:\n
            -----------------------\n
            🎫 Id de la Transacción: {payment_response.transaction_id}\n
            💵 Valor Total: {payment_response.transaction_amount} {payment_response.currency}\n
            🗓️ Fecha: {payment_response.created_at}
            💳 Método de pago: Pagaste con tu {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}
            -----------------------\n
            ¡Gracias por tu compra 🙋‍♂️!
        """
        
    async def failed_payment_template(self, payment_data: PaymentData, payment_response: PaymentResponse) -> str:
        return f"""
            **Tu pago fue rechazado 🥲**\n\n
            ¡Hola {payment_data.user_data.first_name}!\n
            
            Datos de la compra:\n
            -----------------------\n
            🎫 Id de la transacción: {payment_response.transaction_id}\n
            💵 Valor Total: {payment_response.transaction_amount} {payment_response.currency}\n
            🗓️ Fecha: {payment_response.created_at}\n
            💳 Motivo: Saldo insuficiente en tú {payment_response.payment_method_id} terminada en {payment_response.last_digits_card}\n
            -----------------------\n
           ¡Por favor intenta nuevamente 😉!
        """
    