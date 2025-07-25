from engine.app.repositories.models.payment import PaymentModel

from pynamodb.exceptions import DoesNotExist
import logging


log = logging.getLogger("payment." + __name__)



class PaymentRepository:

    def create(self, payment):

        payment_model = PaymentModel(
            id=payment.id,
            order_id=payment.order_id,
            additional_data=payment.additional_data,
            title=payment.title,
            status=payment.status,
            qr_data=payment.qr_data,
        )

        payment_model.save()

        payment.updated_at = payment_model.updated_at
        payment.created_at = payment_model.created_at

        return payment

    def get_payment(self, payment_entity, identifier):
        try:
            payment_model = PaymentModel.get(identifier)
        except DoesNotExist:
            log.info(f"Payment id #{identifier} not found, trying with order_id...")
            try:
                payment_model = next(PaymentModel.scan(PaymentModel.order_id == identifier))
            except StopIteration:
                log.warning(f"Payment with order_id or id #{identifier} not found")
                return None

        return payment_entity(
            id=payment_model.id,
            order_id=payment_model.order_id,
            additional_data=payment_model.additional_data,
            qr_data=payment_model.qr_data,
            created_at=payment_model.created_at,
            updated_at=payment_model.updated_at,
            title=payment_model.title,
            status=payment_model.status,
        )

    def update_status(self, payment_entity, order_id, status):
        try:
            try:
                payment_model = next(PaymentModel.scan(PaymentModel.order_id == order_id))
            except StopIteration:
                log.warning(f"Payment with order_id #{order_id} not found")
                return None

            payment_model.update(actions=[PaymentModel.status.set(status)])

            return payment_entity(
                id=payment_model.id,
                order_id=payment_model.order_id,
                additional_data=payment_model.additional_data,
                qr_data=payment_model.qr_data,
                created_at=payment_model.created_at,
                updated_at=payment_model.updated_at,
                title=payment_model.title,
                status=payment_model.status,
            )

        except Exception as e:
            log.error(f"Error updating payment status: {e}")
            return None
