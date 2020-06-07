from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length


class SendMailSchema(Schema):
    email = fields.Email(required=True, validate=Length(min=3, max=50))
    message = fields.String(required=True, validate=Length(min=5, max=100))
