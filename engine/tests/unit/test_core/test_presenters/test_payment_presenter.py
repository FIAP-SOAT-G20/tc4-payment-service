from engine.app.core.presenters.payment.paymentPresenter import PaymentPresenter
from engine.tests.unit import PaymentUnitTest

from datetime import datetime
from types import SimpleNamespace


class TestPaymentPresenter(PaymentUnitTest):

    def setUp(self):
        self.payment_mock = SimpleNamespace(
            id="pay_123",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at="",
            order_id="order_456",
            additional_data='{"customer":"John"}',
            title="Payment Title",
            status="CONFIRMED",
            qr_data="some_qr_data"
        )
        super(TestPaymentPresenter, self).setUp()

    def test_present_valid_json_additional_data(self):
        result = PaymentPresenter.present(self.payment_mock)

        self.assertEqual(result["id"], "pay_123")
        self.assertEqual(result["order_id"], "order_456")
        self.assertEqual(result["status"], "CONFIRMED")
        self.assertEqual(result["title"], "Payment Title")
        self.assertEqual(result["qr_data"], "some_qr_data")
        self.assertEqual(result["additional_data"], {"customer": "John"})
        self.assertEqual(result["created_at"], self.payment_mock.created_at)

    def test_present_invalid_json_additional_data(self):
        self.payment_mock.additional_data = "{not-valid-json}"  # quebra o json.loads

        result = PaymentPresenter.present(self.payment_mock)

        self.assertEqual(result["additional_data"], "{not-valid-json}")  # string pura
        self.assertEqual(result["id"], "pay_123")  # outros campos ainda OK

    def test_present_additional_data_is_none(self):
        self.payment_mock.additional_data = None

        result = PaymentPresenter.present(self.payment_mock)

        self.assertIsNone(result["additional_data"])
        self.assertEqual(result["id"], "pay_123")

    def test_present_preserves_all_fields_even_on_error(self):
        self.payment_mock.additional_data = "not-a-json"
        result = PaymentPresenter.present(self.payment_mock)

        self.assertIn("id", result)
        self.assertIn("order_id", result)
        self.assertIn("status", result)
        self.assertIn("additional_data", result)

