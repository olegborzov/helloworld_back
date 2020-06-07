from enum import Enum
from functools import wraps
from typing import Type

from flask import request, g
from marshmallow import Schema, ValidationError, EXCLUDE

from app_web.utils.response_json import marshmallow_errors, bad_request


class TargetEnum(Enum):
    args = 1
    json = 2


class RequestValidator:
    """
    Validate request with marshmallow schema
    """
    def __init__(self, schema: Type[Schema], target: TargetEnum, many: bool = False,
                 partial: bool = False, empty: bool = False):
        self._target = target
        self._schema = schema
        self._many = many
        self._partial = partial
        self._empty = empty

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            target_data = request.args.to_dict() if self._target == TargetEnum.args else request.json

            if not target_data and not self._empty:
                return bad_request(f'No request {self._target} provided')
            elif self._empty and target_data is None:
                target_data = {}

            schema = self._schema(partial=self._partial, many=self._many)

            try:
                validated_data = schema.load(target_data, unknown=EXCLUDE)
            except ValidationError as err:
                return marshmallow_errors(err.messages)

            setattr(g, f'validated_{self._target.name}', validated_data)

            return func(*args, **kwargs)

        return wrapper


def validate_request_json(schema: Type[Schema], many: bool = False, partial: bool = False, empty: bool = False):
    """
    Validate request json with marshmallow schema
    """
    return RequestValidator(schema=schema, target=TargetEnum.json, many=many, partial=partial, empty=empty)


def validate_request_args(schema: Type[Schema], partial: bool = False, empty: bool = False):
    """
    Validate request args with marshmallow schema
    """
    return RequestValidator(schema=schema, target=TargetEnum.args, many=False, partial=partial, empty=empty)
