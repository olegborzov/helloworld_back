from functools import wraps

from flask_login import current_user

from app_web.utils import response_json


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            msg = 'Пользователь не авторизован'
            return response_json.not_authorized(msg)
        return func(*args, **kwargs)

    return wrapper


def authorized_denied(func):
    """
    Return 403 FORBIDDEN if user is authorized
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            msg = 'Пользователь авторизован'
            return response_json.forbidden(msg)
        return func(*args, **kwargs)

    return wrapper
