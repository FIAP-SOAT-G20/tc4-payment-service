from engine.app.core.usecases.payment.checkout import CheckoutUseCase
from engine.app.core.presenters.payment.paymentPresenter import PaymentPresenter
from engine.app.repositories.paymentRepository import PaymentRepository
from engine.app.services.mercado_pago.qrcodeService import MercadoPagoService
from engine.app.services.amazon_sns.snsService import SNSService

import json


class CheckoutController:
    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.presenter = PaymentPresenter()
        self.mercado_pago_service = MercadoPagoService()
        self.amazon_sns_service = SNSService()
        self.payment_use_case = CheckoutUseCase(self.payment_repository, self.presenter,
                                                self.mercado_pago_service, self.amazon_sns_service)


    def do_checkout(self, order_id, callback_url, additional_data={}):
        payment = self.payment_use_case.perform_checkout(order_id, callback_url, json.dumps(additional_data))
        return payment

    def process_callback(self, jdata):
        payment = self.payment_use_case.process_callback(jdata)
        return payment
