from flask import jsonify, request, url_for
import logging
import json

from engine.app.external.flask.routes import api
from engine.app.core.controllers.payment.checkoutController import CheckoutController
from engine.app.core.controllers.payment.viewerController import PaymentViewerController
from engine.app.external.marshmallow.validator import ValidationData
from engine.app.external.marshmallow.schemas.callbackSchema import CallbackSchema

log = logging.getLogger("payment." + __name__)

checkout_use_case = CheckoutController()
viewer_use_case = PaymentViewerController()


@api.route('/payments', methods=['GET'])
def get_payments():
    payments = viewer_use_case.get_all_payments(limit=request.args.get('limit', 10))
    return jsonify(payments)


@api.route('/payments/<string:order_id>/checkout', methods=['POST'])
def checkout(order_id):
    additional_data = request.json
    try:
        payment = checkout_use_case.do_checkout(order_id, url_for('api.payment_callback', _external=True), additional_data)
        return jsonify({"status": "success", "data": payment}), 201
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400


@api.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = viewer_use_case.get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment)
    return jsonify({"status": "error", "error": "Payment not found"}), 404


@api.route('/payments/callback', methods=['POST'])
def payment_callback():
    data = json.loads(request.data.decode())
    ValidationData(CallbackSchema, data)
    payment = checkout_use_case.process_callback(data)
    return jsonify({"status": "success", "data": payment}), 200
