import logging
import os
from behave import fixture, use_fixture

from engine import app

log = logging.getLogger("payment.{}".format(__name__))


@fixture
def app_client(context, *args, **kwargs):
    log.info("Initial test config")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app_context = app.test_request_context()
    app_context.push()
    context.client = app.test_client()
    yield context.client


def before_all(context):
    log.info(f"Before all")
    os.environ['BEHAVE_TESTS_RUNNING'] = 'true'
    use_fixture(app_client, context)


def before_feature(context, feature):
    log.info("#######################################################################")
    log.info(f"Before Feature: {feature}")
    log.info("#######################################################################")


def after_feature(context, feature):
    log.info(f"After Feature: {feature}")


def before_scenario(context, scenario):
    log.info("#######################################################################")
    log.info(f"Before Scenario: {scenario}")
    log.info("#######################################################################")


def after_scenario(context, scenario):
    log.info(f"After Scenario {scenario}")