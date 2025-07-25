import requests
import os


class MercadoPagoService:

    def __init__(self):
        self.base_url = os.getenv("MERCADO_PAGO_URL", "http://localhost:3001/mercadopago/instore/orders/qr")

    def get_qr_code(self, order_id, title, callback_url):
        payload = {
            "external_reference": order_id,
            "notification_url": callback_url,
            "title": title
        }

        response = requests.post(self.base_url, json=payload)

        if response.status_code != 200:
            raise Exception(f"Error from Mercado Pago API: Status {response.status_code}")

        response_data = response.json()

        if response_data.get('in_store_order_id') != order_id:
            return None

        return response_data["qr_data"]
