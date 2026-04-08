from core import INotificationChannel
from schemas import PurchaseDetailsModel

class WhatsappChannel(INotificationChannel):
    async def notify(self, purchase_details: PurchaseDetailsModel) -> bool:
        """
        Sends a notifications to the user via WhatsApp.
        """
        # Simulating sending a message via WhatsApp.
        if purchase_details.user_data.contac_info.phone_number:
            print(
                f"""
                ¡Hola{purchase_details.user_data.first_name}!\n\n
                Datos de tu compra:\n
                -----------------\n
                Valor total: {purchase_details.amount_purchase}\n
                Método de pago: {purchase_details.payment_method}\n\n
                Gracias por tu compra.
                """
            )
            return True
        return False
    
class SmsChannel(INotificationChannel):
    async def notify(self, purchase_details: PurchaseDetailsModel) -> bool:
        """
        Sends a notifications to user via SMS.
        """
        if purchase_details.user_data.contac_info.phone_number:
            # Simulating sending a message via SMS.
            print(
                f"""
                ¡Hola{purchase_details.user_data.first_name}!\n\n
                Datos de tu compra:\n
                -----------------\n
                Valor total: {purchase_details.amount_purchase}\n
                Método de pago: {purchase_details.payment_method}\n\n
                Gracias por tu compra.
                """
            )
            return True
        return False   
    
class EmailChannel(INotificationChannel):
    async def notify(self, purchase_details: PurchaseDetailsModel) -> bool:
        """
        Sends a notifications to the user via email.
        """
        if purchase_details.user_data.contac_info.email:
            message_body = f"""
            ¡Hola {purchase_details.user_data.first_name}!

            Datos de tu compra:
            -------------------------
            Valor total: ${purchase_details.amount_purchase}
            Método de pago: {purchase_details.payment_method}

            Gracias por tu compra.
            """
            # Simulating sending a message via email.
            from email.mime.text import MIMEText
            mensaje_email = MIMEText(message_body, 'plain', 'utf-8')

            mensaje_email['Subject'] = "Confirmación de tu compra"
            mensaje_email['From'] = "tienda@d1.com"
            mensaje_email['To'] = purchase_details.user_data.contac_info.email
            return True
        return False
    
    