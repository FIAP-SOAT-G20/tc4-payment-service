from flask import request, abort
from marshmallow import ValidationError
from functools import wraps

import logging

log = logging.getLogger("payment." + __name__)


def validate_request(schema):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            ValidationData(schema, request.json)
            return func(*args, **kwargs)
        return wrap
    return wrapper


class ValidationData:

    def __init__(self, schema, json_data):
        try:
            schema().load(json_data)
            return
        except ValidationError as err:
            log.error(err)
            abort(400, err.messages)
