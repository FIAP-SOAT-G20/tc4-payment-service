from engine.app.core.usecases.payment.viewer import PaymentViewerUseCase
from engine.app.core.presenters.payment.paymentPresenter import PaymentPresenter
from engine.app.repositories.paymentRepository import PaymentRepository


class PaymentViewerController:

    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.presenter = PaymentPresenter()
        self.payment_use_case = PaymentViewerUseCase(self.payment_repository, self.presenter)

    def get_payment_by_id(self, payment_id):
        return self.payment_use_case.get_payment_by_id(payment_id)