# from services.cart import ShoppingCart
# from schemas import AmountPurchasedModel

# def procesar_pago(metodo, monto):
#     if metodo == "tarjeta":
#         print(f"Pagando {monto} con tarjeta de crédito")
#     elif metodo == "paypal":
#         print(f"Pagando {monto} con PayPal")
#     elif metodo == "crypto":
#         print(f"Pagando {monto} con Bitcoin")


# cart = ShoppingCart()

# print(cart.calculate_total(AmountPurchasedModel(amount=60000), "black friday"))

# from core import get_processing_network


# print(get_processing_network(343201))

# from services.validators import CardValidator

# # num = 343201
# # print(len(str(num)))

# validor = CardValidator()

# print(validor.validate(4242424242424242))

# from collections import deque


# queue: deque[tuple[str, int]] = deque()

# def enqueue(elemtents) -> None:
#     [queue.append(el) for el in elemtents]
# from core import dequeue
# from schemas import PurchaseDetailsModel, UserModel, ContactInfoModel

# contact_info = ContactInfoModel(email="juan@example.com", phone_number="3238647590")
# user = UserModel(first_name="juan", middle_name="stiven", first_surname="cabrales", middle_surname="jonuazo", contac_info=contact_info)

# purchase_details = PurchaseDetailsModel(user_data=user, amount_purchase=5000, payment_method='tarjeta', transaction_id=4) # type: ignore
# print(dequeue(NOTIFICATIONS_QUEUE, purchase_details))

num = "8855656223"

bin = num[:4]
print(bin)