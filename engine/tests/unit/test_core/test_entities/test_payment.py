from datetime import datetime

from engine.tests.unit import PaymentUnitTest
from engine.app.core.entities.payment import Payment


class TestPaymentEntity(PaymentUnitTest):

    payment_data = {
        "id": "payment123",
        "created_at": datetime.utcnow(),
        "order_id": "order456",
        "additional_data": '{"customer":"test"}',
        "title": "Test Payment",
        "status": "PROCESSING"
    }

    def test_payment_initialization(self):
        payment = Payment(**self.payment_data)

        self.assertEqual(payment.id, "payment123")
        self.assertEqual(payment.order_id, "order456")
        self.assertEqual(payment.additional_data, '{"customer":"test"}')
        self.assertEqual(payment.title, "Test Payment")
        self.assertEqual(payment.status, "PROCESSING")
        self.assertEqual(payment.updated_at, "")
        self.assertEqual(payment.qr_data, "")

        self.assertIsInstance(payment.created_at, datetime)

    def test_status_setter_valid_values(self):
        payment = Payment(**self.payment_data)

        for valid_status in ["PROCESSING", "CONFIRMED", "FAILED", "ABORTED"]:
            payment.status = valid_status
            self.assertEqual(payment.status, valid_status)

    def test_status_setter_invalid_value_raises(self):
        payment = Payment(**self.payment_data)

        with self.assertRaises(ValueError) as context:
            payment.status = "INVALID_STATUS"

        self.assertEqual(str(context.exception), "Invalid status")

    def test_status_property_isolation(self):
        payment = Payment(**self.payment_data)
        self.assertEqual(payment._status, "PROCESSING")
        self.assertEqual(payment.status, "PROCESSING")

        payment.status = "CONFIRMED"
        self.assertEqual(payment.status, "CONFIRMED")
        self.assertEqual(payment._status, "CONFIRMED")

    def test_optional_fields_are_optional(self):
        payment = Payment(
            id="abc",
            created_at=datetime.utcnow(),
            order_id="123",
            additional_data="{}",
            title="No optional",
            status="FAILED"
        )

        self.assertEqual(payment.updated_at, "")
        self.assertEqual(payment.qr_data, "")

