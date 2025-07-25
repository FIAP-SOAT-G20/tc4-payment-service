from engine.app.core.entities.payment import Payment


class PaymentViewerUseCase:

    def __init__(self, repository, presenter):
        self.repository = repository
        self.presenter = presenter

    def get_payment_by_id(self, payment_id):
        payment = self.repository.get_payment(Payment, payment_id)
        return self.presenter.present(payment)
