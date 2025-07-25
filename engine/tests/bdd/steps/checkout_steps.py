from unittest import TestCase
from unittest.mock import patch, MagicMock
from behave import step, register_type
import logging
from flask import url_for
from datetime import datetime, timezone

from engine.tests.bdd.utils import parse_unquoted

tc = TestCase()
register_type(Unquoted=parse_unquoted)
log = logging.getLogger("payment.{}".format(__name__))

@step(u'enviar um pedido ao checkout')
@patch('engine.app.repositories.paymentRepository.PaymentModel')
@patch('engine.app.services.mercado_pago.qrcodeService.requests')
def step_impl(context, mock_requests, paymentModelMock):
    log.info(f"{'-' * 80}\n[BEHAVE] Quando enviar um pedido ao checkout")

    model_mock = paymentModelMock()

    model_mock.save.return_value = True
    model_mock.updated_at = datetime.now(timezone.utc)
    model_mock.created_at = datetime.now(timezone.utc)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'qr_data': 'behave_qr_data', 'in_store_order_id': 'behave_order_id'}

    mock_requests.post.return_value = mock_response

    tc.assertTrue(context.client, "Não existe instância válida para execução do teste")
    url = url_for('api.checkout', order_id="behave_order_id")
    response = context.client.post(url, follow_redirects=True, json={})

    tc.assertIsNotNone(response, f"Retorno invalido {response}")
    context.config.userdata['response'] = response.json



@step(u'a resposta deve conter o campo {campo} no json')
def step_impl(context, campo):
    log.info(f"{'-' * 80}\n[BEHAVE] Então a resposta deve conter o campo {campo} no json")
    response = context.config.userdata['response']

    data = response.get("data", {})
    tc.assertIn(campo, data, f"O campo '{campo}' não está presente no JSON de resposta.")


