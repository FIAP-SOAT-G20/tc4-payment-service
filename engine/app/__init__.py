from flask import Flask
from flasgger import Swagger
import logging
import os

from engine.app.configs import NAME, VERSION, STARTED_AT
from engine.app.configs.environment import get_config_by_environment
from engine.app.configs.log import configure_logging
from engine.app.repositories.models.default import BaseModel
from engine.app.repositories.models.payment import PaymentModel
from engine.app.external.flask.routes import api

log = logging.getLogger("payment." + __name__)


def create_app():
    app = Flask(__name__)

    log.info("Configuring flask app")

    log.info("Loading log configuration")
    configure_logging(os.environ)

    log.info("Loading environment configuration")
    app.config.from_object(get_config_by_environment(os.environ))

    log.info("Initializing Swagger API documentation")

    Swagger(app, template_file='../apidocs.yaml')

    log.info("Registering routes")
    app.register_blueprint(api)

    log.info("Configuring DynamoDB on model")
    BaseModel.Meta.host = app.config['DYNAMODB_SETTINGS']['host']
    BaseModel.Meta.region = app.config['DYNAMODB_SETTINGS']['region']
    if not PaymentModel.exists():
        PaymentModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True
        )

    log.info(f"{NAME}:{VERSION} Server Started Successfully at {STARTED_AT}")

    return app
