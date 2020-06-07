from flask import g
from flask_login import login_user, logout_user, current_user

from app_web.schemas.auth import LoginSchema, UserSchema, RegisterSchema
from app_web.utils.decorators import authorized_denied, login_required
from app_web.utils.response_json import success, bad_request, not_authorized
from app_web.utils.validate_request import validate_request_json
from core.registry import login_manager, db
from models import User


@login_manager.user_loader
def user_loader(user_id) -> User:
    return db.session.query(User).get(int(user_id))


def me():
    if current_user.is_authenticated:
        return success(UserSchema().dump(current_user))

    return not_authorized('Вы не авторизованы')


@authorized_denied
@validate_request_json(LoginSchema)
def login():
    data = g.validated_json

    user = User.get_by_email(data['email'])
    if not user:
        return not_authorized('Пользователь с данным email не найден')

    if not user.verify_password(data['password']):
        return not_authorized('Неправильный пароль')

    login_user(user, remember=data['remember_me'])
    return success(UserSchema().dump(user))


@authorized_denied
@validate_request_json(RegisterSchema)
def register():
    data = g.validated_json

    user = User.get_by_email(data['email'])
    if user:
        return bad_request("Пользователь с данным email уже существует")

    user = User.create(email=data['email'], password=data['password'])
    login_user(user, remember=True)
    return success(UserSchema().dump(user))


@login_required
def logout():
    logout_user()
    return success(True)
