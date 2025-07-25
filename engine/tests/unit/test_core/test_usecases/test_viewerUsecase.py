from unittest.mock import MagicMock

from engine.tests.unit import PaymentUnitTest
from engine.app.core.usecases.payment.viewer import PaymentViewerUseCase
from engine.app.core.entities.payment import Payment


class TestPaymentViewerUseCase(PaymentUnitTest):

    def setUp(self):
        self.repository = MagicMock()
        self.presenter = MagicMock()
        self.usecase = PaymentViewerUseCase(self.repository, self.presenter)
        self.payment_id = "payment123"

    def test_get_payment_by_id_success(self):
        payment_mock = Payment(
            id="payment123",
            order_id="order456",
            additional_data="{}",
            created_at=None,
            title="Test",
            status="CONFIRMED"
        )
        self.repository.get_payment.return_value = payment_mock
        self.presenter.present.return_value = {"id": "payment123", "status": "CONFIRMED"}

        result = self.usecase.get_payment_by_id(self.payment_id)

        self.repository.get_payment.assert_called_once_with(Payment, self.payment_id)
        self.presenter.present.assert_called_once_with(payment_mock)
        self.assertEqual(result, {"id": "payment123", "status": "CONFIRMED"})

        super(TestPaymentViewerUseCase, self).setUp()

    def test_get_payment_by_id_returns_none(self):
        self.repository.get_payment.return_value = None
        self.presenter.present.return_value = None

        result = self.usecase.get_payment_by_id(self.payment_id)

        self.repository.get_payment.assert_called_once()
        self.presenter.present.assert_called_once_with(None)
        self.assertIsNone(result)

    def test_get_payment_by_id_repository_raises_exception(self):
        self.repository.get_payment.side_effect = Exception("DB error")

        with self.assertRaises(Exception) as context:
            self.usecase.get_payment_by_id(self.payment_id)

        self.repository.get_payment.assert_called_once()
        self.assertEqual(str(context.exception), "DB error")
        self.presenter.present.assert_not_called()

