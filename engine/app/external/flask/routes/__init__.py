from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from engine.app.external.flask.routes.payment import endpoints
