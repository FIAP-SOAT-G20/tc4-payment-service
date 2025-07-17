from engine.app.core.entities.payment import Payment
from datetime import datetime, timezone
import logging
from uuid import uuid4

log = logging.getLogger("payment." + __name__)


class CheckoutUseCase:

    def __init__(self, repository, presenter, qr_code_service, notification_service):
        self.repository = repository
        self.presenter = presenter
        self.qr_code_service = qr_code_service
        self.notification_service = notification_service

    def perform_checkout(self, order_id, callback_url, additional_data):

        title = f"Mercado Pago - Order #{order_id}"

        payment = Payment(
            id=str(uuid4()),
            order_id=order_id,
            additional_data=str(additional_data),
            created_at=datetime.now(timezone.utc),
            title=title,
            status="PROCESSING"
        )

        try:
            qr_data = self.qr_code_service.get_qr_code(order_id, title, callback_url)
            if qr_data:
                payment.qr_data = qr_data
                log.info(f"QR Code successfully retrieved for Order #{order_id}")
            else:
                payment.status = "FAILED"
                log.info(f"QR Code failed to retrieved for Order #{order_id}")
        except Exception as e:
            log.error(f"Error retrieving QR Code for Order #{order_id}: {e}")
            payment.status = "ABORTED"

        payment = self.repository.create(payment)

        return self.presenter.present(payment)

    def process_callback(self, data):
        try:
            payment = self.repository.update_status(Payment, data['resource'], "CONFIRMED")
        except Exception as e:
            log.error(f"Error updating payment status: {e}")
            return False

        try:
            self.notification_service.send_notification("payment-approved", "CONFIRMED", f"Order #{data['resource']}")
        except Exception as e:
            log.error(f"Error sending notification: {e}")
            log.info("Trying to send notification again...")
            try:
                self.notification_service.send_notification("payment-approved", "CONFIRMED",
                                                            f"Order #{data['resource']}")
            except Exception as e:
                log.error(f"Error sending second notification: {e}")

        return self.presenter.present(payment)
