from unittest.mock import patch, MagicMock
from engine.tests.unit import PaymentUnitTest
from engine.app.services.mercado_pago.qrcodeService import MercadoPagoService


class TestMercadoPagoService(PaymentUnitTest):

    def setUp(self):
        self.service = MercadoPagoService()
        self.order_id = "order123"
        self.title = "Test Title"
        self.callback_url = "https://callback.url"

        super(TestMercadoPagoService, self).setUp()

    @patch("engine.app.services.mercado_pago.qrcodeService.requests.post")
    def test_get_qr_code_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "in_store_order_id": self.order_id,
            "qr_data": "mocked_qr_data"
        }

        mock_post.return_value = mock_response

        result = self.service.get_qr_code(self.order_id, self.title, self.callback_url)

        self.assertEqual(result, "mocked_qr_data")
        mock_post.assert_called_once_with(
            self.service.base_url,
            json={
                "external_reference": self.order_id,
                "notification_url": self.callback_url,
                "title": self.title
            }
        )

    @patch("engine.app.services.mercado_pago.qrcodeService.requests.post")
    def test_get_qr_code_mismatched_order_id_returns_none(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "in_store_order_id": "wrong_id",
            "qr_data": "qr_should_be_ignored"
        }

        mock_post.return_value = mock_response

        result = self.service.get_qr_code(self.order_id, self.title, self.callback_url)

        self.assertIsNone(result)

    @patch("engine.app.services.mercado_pago.qrcodeService.requests.post")
    def test_get_qr_code_api_error_raises_exception(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.service.get_qr_code(self.order_id, self.title, self.callback_url)

        self.assertIn("Error from Mercado Pago API", str(context.exception))
