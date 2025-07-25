from unittest.mock import MagicMock, patch
from datetime import datetime

from engine.tests.unit import PaymentUnitTest
from engine.app.core.usecases.payment.checkout import CheckoutUseCase
from engine.app.core.entities.payment import Payment


class TestCheckoutUseCase(PaymentUnitTest):

    def setUp(self):

        self.repository = MagicMock()
        self.presenter = MagicMock()
        self.qr_service = MagicMock()
        self.notification_service = MagicMock()

        self.usecase = CheckoutUseCase(
            repository=self.repository,
            presenter=self.presenter,
            qr_code_service=self.qr_service,
            notification_service=self.notification_service
        )

        self.order_id = "order123"
        self.callback_url = "https://callback.url"
        self.additional_data = {"customer": "test"}

        super(TestCheckoutUseCase, self).setUp()

    @patch("engine.app.core.usecases.payment.checkout.uuid4", return_value="mock-uuid")
    @patch("engine.app.core.usecases.payment.checkout.datetime")
    def test_perform_checkout_success(self, mock_datetime, mock_uuid):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        self.qr_service.get_qr_code.return_value = "mock-qr-code"
        self.repository.create.side_effect = lambda p: p
        self.presenter.present.side_effect = lambda p: {"presented": True, "id": p.id}

        result = self.usecase.perform_checkout(self.order_id, self.callback_url, self.additional_data)

        self.assertTrue(result["presented"])
        self.assertEqual(result["id"], "mock-uuid")
        self.qr_service.get_qr_code.assert_called_once()
        self.repository.create.assert_called_once()
        self.assertEqual(self.presenter.present.call_count, 1)

    @patch("engine.app.core.usecases.payment.checkout.uuid4", return_value="mock-uuid")
    @patch("engine.app.core.usecases.payment.checkout.datetime")
    def test_perform_checkout_qr_none_sets_failed_status(self, mock_datetime, mock_uuid):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        self.qr_service.get_qr_code.return_value = None
        self.repository.create.side_effect = lambda p: p
        self.presenter.present.side_effect = lambda p: p

        result = self.usecase.perform_checkout(self.order_id, self.callback_url, self.additional_data)

        self.assertEqual(result.status, "FAILED")

    @patch("engine.app.core.usecases.payment.checkout.uuid4", return_value="mock-uuid")
    @patch("engine.app.core.usecases.payment.checkout.datetime")
    def test_perform_checkout_qr_exception_sets_aborted_status(self, mock_datetime, mock_uuid):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        self.qr_service.get_qr_code.side_effect = Exception("QR service error")
        self.repository.create.side_effect = lambda p: p
        self.presenter.present.side_effect = lambda p: p

        result = self.usecase.perform_checkout(self.order_id, self.callback_url, self.additional_data)

        self.assertEqual(result.status, "ABORTED")

    def test_process_callback_success(self):
        payment = MagicMock(order_id="order123")
        self.repository.update_status.return_value = payment
        self.presenter.present.return_value = {"status": "ok"}

        result = self.usecase.process_callback({"resource": "some-id"})

        self.repository.update_status.assert_called_once_with(Payment, "some-id", "CONFIRMED")
        self.notification_service.send_notification.assert_called_once()
        self.assertEqual(result["status"], "ok")

    def test_process_callback_update_status_fails(self):
        self.repository.update_status.side_effect = Exception("DB error")

        result = self.usecase.process_callback({"resource": "some-id"})

        self.assertFalse(result)
        self.repository.update_status.assert_called_once()

    def test_process_callback_notification_fails_once_then_success(self):
        payment = MagicMock(order_id="order123")
        self.repository.update_status.return_value = payment
        self.notification_service.send_notification.side_effect = [Exception("1st fail"), None]
        self.presenter.present.return_value = {"status": "ok"}

        result = self.usecase.process_callback({"resource": "res-id"})

        self.assertEqual(self.notification_service.send_notification.call_count, 2)
        self.assertEqual(result["status"], "ok")

    def test_process_callback_notification_fails_twice(self):
        payment = MagicMock(order_id="order123")
        self.repository.update_status.return_value = payment
        self.notification_service.send_notification.side_effect = [Exception("fail1"), Exception("fail2")]
        self.presenter.present.return_value = {"status": "ok"}

        result = self.usecase.process_callback({"resource": "res-id"})

        self.assertEqual(self.notification_service.send_notification.call_count, 2)
        self.assertEqual(result["status"], "ok")

