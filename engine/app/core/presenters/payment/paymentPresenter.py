import json


class PaymentPresenter:
    @staticmethod
    def present(payment):
        try:
            return {
                "id": payment.id,
                "created_at": payment.created_at,
                "updated_at": payment.updated_at,
                "order_id": payment.order_id,
                "additional_data": json.loads(payment.additional_data),
                "title": payment.title,
                "status": payment.status,
                "qr_data": payment.qr_data
            }
        except Exception as e:
            return {
                "id": payment.id,
                "created_at": payment.created_at,
                "updated_at": payment.updated_at,
                "order_id": payment.order_id,
                "additional_data": payment.additional_data,
                "title": payment.title,
                "status": payment.status,
                "qr_data": payment.qr_data
            }

