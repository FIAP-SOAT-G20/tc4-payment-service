from unittest.mock import patch, MagicMock
from engine.tests.unit import PaymentUnitTest
from engine.app.repositories.paymentRepository import PaymentRepository


class TestPaymentRepository(PaymentUnitTest):

    def setUp(self):
        super().setUp()
        self.repo = PaymentRepository()
        self.payment_mock = MagicMock()
        self.payment_mock.id = "123"
        self.payment_mock.order_id = "order123"
        self.payment_mock.additional_data = {"info": "test"}
        self.payment_mock.title = "Test Payment"
        self.payment_mock.status = "CREATED"
        self.payment_mock.qr_data = "QR123"

    @patch("engine.app.repositories.paymentRepository.PaymentModel")
    def test_create_payment_success(self, mock_model):
        mock_instance = MagicMock()
        mock_instance.updated_at = "2024-01-01T00:00:00Z"
        mock_instance.created_at = "2024-01-01T00:00:00Z"
        mock_model.return_value = mock_instance

        result = self.repo.create(self.payment_mock)

        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.payment_mock)
        self.assertEqual(result.updated_at, "2024-01-01T00:00:00Z")
        self.assertEqual(result.created_at, "2024-01-01T00:00:00Z")

    @patch("engine.app.repositories.paymentRepository.PaymentModel")
    def test_get_payment_by_id_success(self, mock_model):
        mock_model.get.return_value = MagicMock(
            id="123", order_id="order123", additional_data={"info": "test"},
            qr_data="qrdata", created_at="created", updated_at="updated",
            title="title", status="status"
        )

        PaymentEntity = MagicMock()
        result = self.repo.get_payment(PaymentEntity, "123")

        mock_model.get.assert_called_once_with("123")
        PaymentEntity.assert_called_once()

    @patch("engine.app.repositories.paymentRepository.PaymentModel.get", side_effect=Exception("boom"))
    def test_get_payment_by_id_and_order_id_not_found(self, mock_get):
        from pynamodb.exceptions import DoesNotExist
        mock_get.side_effect = DoesNotExist()

        with patch("engine.app.repositories.paymentRepository.PaymentModel.scan", return_value=iter([])) as mock_scan:
            PaymentEntity = MagicMock()
            result = self.repo.get_payment(PaymentEntity, "id-not-found")

            mock_scan.assert_called_once()
            self.assertIsNone(result)

    @patch("engine.app.repositories.paymentRepository.PaymentModel.get", side_effect=Exception("boom"))
    def test_get_payment_by_order_id_success(self, mock_get):
        from pynamodb.exceptions import DoesNotExist
        mock_get.side_effect = DoesNotExist()

        payment_model_mock = MagicMock(
            id="123", order_id="order123", additional_data={}, qr_data="qr",
            created_at="created", updated_at="updated", title="title", status="status"
        )

        with patch("engine.app.repositories.paymentRepository.PaymentModel.scan", return_value=iter([payment_model_mock])):
            PaymentEntity = MagicMock()
            result = self.repo.get_payment(PaymentEntity, "fallback-id")

            PaymentEntity.assert_called_once_with(
                id="123", order_id="order123", additional_data={}, qr_data="qr",
                created_at="created", updated_at="updated", title="title", status="status"
            )
            self.assertIsNotNone(result)

    @patch("engine.app.repositories.paymentRepository.PaymentModel.scan", return_value=iter([]))
    def test_update_status_payment_not_found(self, mock_scan):
        PaymentEntity = MagicMock()
        result = self.repo.update_status(PaymentEntity, "order123", "PAID")

        self.assertIsNone(result)

    @patch("engine.app.repositories.paymentRepository.PaymentModel.scan")
    def test_update_status_success(self, mock_scan):
        model_mock = MagicMock(
            id="123", order_id="order123", additional_data={"data": 1}, qr_data="qr",
            created_at="created", updated_at="updated", title="title", status="status"
        )
        mock_scan.return_value = iter([model_mock])

        PaymentEntity = MagicMock()
        result = self.repo.update_status(PaymentEntity, "order123", "PAID")

        model_mock.update.assert_called_once()
        PaymentEntity.assert_called_once_with(
            id="123", order_id="order123", additional_data={"data": 1}, qr_data="qr",
            created_at="created", updated_at="updated", title="title", status="status"
        )
        self.assertEqual(result, PaymentEntity.return_value)

    @patch("engine.app.repositories.paymentRepository.PaymentModel.scan", side_effect=Exception("update exploded"))
    def test_update_status_exception(self, mock_scan):
        PaymentEntity = MagicMock()
        result = self.repo.update_status(PaymentEntity, "order123", "PAID")

        self.assertIsNone(result)
