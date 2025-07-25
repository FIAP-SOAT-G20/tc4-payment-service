from engine.tests.unit import PaymentUnitTest
from unittest.mock import patch, MagicMock
from engine.app.core.controllers.payment import checkoutController


class TestCheckoutController(PaymentUnitTest):

    @patch('engine.app.core.controllers.payment.checkoutController.CheckoutUseCase')
    def test_controller_do_checkout(self, mock_CheckoutUseCase):
        controller_class = checkoutController.CheckoutController

        mock_usecase = MagicMock()
        mock_usecase.perform_checkout.return_value = True

        mock_CheckoutUseCase.return_value = mock_usecase
        controller = controller_class()
        result = controller.do_checkout("order_id_test", "callback_url_test", {"test": "mock"})


        self.assertTrue(result)
        mock_usecase.perform_checkout.assert_called_once_with("order_id_test", "callback_url_test", '{"test": "mock"}')

    @patch('engine.app.core.controllers.payment.checkoutController.CheckoutUseCase')
    def test_controller_do_checkout_with_empty_additional_data(self, mock_CheckoutUseCase):
        mock_usecase = MagicMock()
        mock_usecase.perform_checkout.return_value = True
        mock_CheckoutUseCase.return_value = mock_usecase

        controller = checkoutController.CheckoutController()
        result = controller.do_checkout("order_id", "callback_url")

        self.assertTrue(result)
        mock_usecase.perform_checkout.assert_called_once_with("order_id", "callback_url", '{}')

    @patch('engine.app.core.controllers.payment.checkoutController.CheckoutUseCase')
    def test_controller_process_callback(self, mock_CheckoutUseCase):
        controller_class = checkoutController.CheckoutController

        mock_usecase = MagicMock()
        mock_usecase.process_callback.return_value = True

        mock_CheckoutUseCase.return_value = mock_usecase
        controller = controller_class()
        result = controller.process_callback("order_id_test")

        self.assertTrue(result)
        mock_usecase.process_callback.assert_called_once_with("order_id_test")



