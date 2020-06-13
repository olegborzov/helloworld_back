from flask_marshmallow import Schema
from flask_marshmallow.fields import fields
from marshmallow.validate import Length


class UserSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "email", "name", "is_admin", "is_guest")


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=Length(min=3, max=50))
    password = fields.String(required=True, validate=Length(min=3, max=50))
    remember_me = fields.Boolean(required=False, default=False, missing=False)


class RegisterSchema(Schema):
    name = fields.String(required=False, validate=Length(min=3, max=50))
    email = fields.Email(required=True, validate=Length(min=3, max=50))
    password = fields.String(required=True, validate=Length(min=3, max=50))
