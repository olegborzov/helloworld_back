from http import HTTPStatus
from unittest.mock import ANY

import pytest
from flask_login import current_user

from core.funcs import have_json
from models import User


########################################
# Test POST /api/auth/login
########################################

def test_login_ok(client):
    res = client.post("/api/auth/login", json={'email': 'admin@test.ru', 'password': 'admin'})
    assert res.status_code == HTTPStatus.OK.value
    assert current_user.is_authenticated
    assert current_user.email == 'admin@test.ru'


def test_login_bad_password(client):
    res = client.post("/api/auth/login", json={'email': 'admin@test.ru', 'password': 'bad_password'})
    assert res.status_code == HTTPStatus.UNAUTHORIZED.value
    assert not current_user.is_authenticated


def test_login_not_exist(client):
    res = client.post("/api/auth/login", json={'email': 'not_found@test.ru', 'password': 'admin'})
    assert res.status_code == HTTPStatus.UNAUTHORIZED.value
    assert not current_user.is_authenticated


def test_login_bad_json(client):
    res = client.post("/api/auth/login", json={'bad_field': 'admin@test.ru', 'not_password': 'admin'})
    assert res.status_code == HTTPStatus.BAD_REQUEST.value
    assert not current_user.is_authenticated


@pytest.mark.usefixtures('auth_admin')
def test_login_already_logged(client):
    res = client.post("/api/auth/login", json={'email': 'admin@test.ru', 'password': 'admin'})
    assert res.status_code == HTTPStatus.FORBIDDEN.value
    assert current_user.is_authenticated
    assert current_user.email == 'admin@test.ru'


########################################
# Test POST /api/auth/logout
########################################

@pytest.mark.usefixtures('auth_admin')
def test_logout_ok(client):
    res = client.post("/api/auth/logout")
    assert res.status_code == HTTPStatus.OK.value
    assert not current_user.is_authenticated


def test_logout_not_logged_in(client):
    res = client.post("/api/auth/logout")
    assert res.status_code == HTTPStatus.UNAUTHORIZED.value
    assert not current_user.is_authenticated


########################################
# Test POST /api/auth/register
########################################


def test_register_ok(client):
    res = client.post("/api/auth/register", json={'email': 'new_user@test.ru', 'password': 'pass'})
    assert res.status_code == HTTPStatus.OK.value
    assert current_user.is_authenticated

    new_user = User.get_by_email('new_user@test.ru')
    assert current_user.id == new_user.id


@pytest.mark.usefixtures('auth_admin')
def test_register_already_logged(client):
    res = client.post("/api/auth/register", json={'email': 'new_user@test.ru', 'password': 'pass'})
    assert res.status_code == HTTPStatus.FORBIDDEN.value
    assert current_user.is_authenticated
    assert current_user.email == 'admin@test.ru'


def test_register_user_already_exist(client):
    res = client.post("/api/auth/register", json={'email': 'admin@test.ru', 'password': 'admin'})
    assert res.status_code == HTTPStatus.BAD_REQUEST.value
    assert not current_user.is_authenticated


def test_register_without_password(client):
    res = client.post("/api/auth/register", json={'email': 'admin@test.ru'})
    assert res.status_code == HTTPStatus.BAD_REQUEST.value
    assert not current_user.is_authenticated

    res = client.post("/api/auth/register", json={'password': 'admin'})
    assert res.status_code == HTTPStatus.BAD_REQUEST.value
    assert not current_user.is_authenticated


########################################
# Test GET /api/auth/me
########################################


@pytest.mark.usefixtures('auth_admin')
def test_get_me_ok(client):
    res = client.get("/api/auth/me")
    assert res.status_code == HTTPStatus.OK.value
    assert res.json['success'] is True

    should_be = {'email': 'admin@test.ru', 'id': ANY, 'is_admin': True, 'is_guest': False}
    assert have_json(res.json['result'], should_be)


def test_get_me_not_logged(client):
    res = client.get("/api/auth/me")
    assert res.status_code == HTTPStatus.UNAUTHORIZED.value
