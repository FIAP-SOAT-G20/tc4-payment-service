from marshmallow import Schema, fields


class CallbackSchema(Schema):

    resource = fields.String(required=True)
    topic = fields.String(required=False, allow_none=True)
