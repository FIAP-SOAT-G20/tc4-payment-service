from engine.tests.unit import PaymentUnitTest
from unittest.mock import patch, MagicMock
from engine.app.core.controllers.payment import viewerController


class TestViewerController(PaymentUnitTest):

    @patch('engine.app.core.controllers.payment.viewerController.PaymentViewerUseCase')
    def test_controller_get_payment_by_id(self, mock_PaymentViewerUseCase):
        controller_class = viewerController.PaymentViewerController

        mock_usecase = MagicMock()
        mock_usecase.get_payment_by_id.return_value = True

        mock_PaymentViewerUseCase.return_value = mock_usecase
        controller = controller_class()
        result = controller.get_payment_by_id("order_id_test")

        self.assertTrue(result)
        mock_usecase.get_payment_by_id.assert_called_once_with("order_id_test")



