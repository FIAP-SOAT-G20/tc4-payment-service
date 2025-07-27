import logging

from datetime import timedelta

log = logging.getLogger("payment." + __name__)

swagger_conf = {
        "swagger": "2.0",
        "info": {
            "title": "API de Pagamento com Mercado Pago",
            "description": "Documentação de API do microserviço de pagamento",
            "version": "1.0"
        },
        "basePath": "/api",
        "swagger_ui_css": "/static/apidocs.css"

}


def get_dynamodb_settings(environment):
    settings = {
        'region': environment.get('AWS_REGION', 'us-east-1'),
        'aws_access_key_id': environment.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': environment.get('AWS_SECRET_ACCESS_KEY')
    }
    return settings


def production_config(environment):
    return type('ProductionConfig', (object,), {
        "DEBUG": False,
        "TESTING": False,
        "DYNAMODB_SETTINGS": get_dynamodb_settings(environment),
        "SECRET_KEY": environment['SECRET_KEY'],
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def development_config(environment):
    return type('DevelopmentConfig', (object,), {
        "DEBUG": True,
        "TESTING": False,
        "DYNAMODB_SETTINGS": get_dynamodb_settings(environment),
        "SECRET_KEY": environment['SECRET_KEY'],
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def testing_config(environment):
    return type('TestingConfig', (object,), {
        "DEBUG": False,
        "TESTING": True,
        "DYNAMODB_SETTINGS": {
            'region': 'us-east-1',
            'host': environment.get('DYNAMODB_ENDPOINT', 'http://192.168.0.16:8000')
        },
        "SECRET_KEY": environment['SECRET_KEY'],
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def get_config_by_environment(environment: dict):
    log.info("Checking app env vars")
    required_keys = ['FLASK_APP', 'ENVIRONMENT', 'SECRET_KEY', 'MERCADO_PAGO_URL']

    log.info("Checking required env vars")
    for key in required_keys:
        if key not in environment.keys():
            exit(f"Missing env var: {key}")

    log.info("Checking optional env vars")
    environment['PERMANENT_SESSION_LIFETIME'] = str(environment.get("PERMANENT_SESSION_LIFETIME", 1460))

    configurations = {
        "development": development_config,
        "production": production_config,
        "testing": testing_config
    }

    env = environment.get('ENVIRONMENT')
    configuration = configurations.get(env)(environment)
    log.info(f"Environment Configuration set to: {env}")
    return configuration
