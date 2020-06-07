# This Python file uses the following encoding: utf-8
"""
Registry managers
"""
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

__all__ = ["DefaultManager", "WebManager"]


class BaseManager:
    def __init__(self):
        managers = getattr(self, "__annotations__", {})
        for field_name, field_class in managers.items():
            setattr(self, field_name, field_class())

        super().__init__()

    def as_dict(self):
        return self.__dict__


class DefaultManager(BaseManager):
    marshmallow: Marshmallow


class WebManager(BaseManager):
    login: LoginManager
    marshmallow: Marshmallow
    cors: CORS
