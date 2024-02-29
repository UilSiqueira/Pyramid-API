import pytest
import json
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])

PATH_REGISTER = '/user/register'
PATH_LOGIN = '/user/login'
HEADERS = {'Content-Type': 'application/json'}


def test_register_user_route(test_client, clear_users_db):
    method = 'POST'
    body = json.dumps({'username': 'JohnDoe', 'password': 'pass#'})

    test_client.request(method, PATH_REGISTER, body, HEADERS)

    response = test_client.getresponse()

    assert response.status == 201


def test_register_user_route_user_already_exists(test_client, user_on_db):
    user_on_db['user'] # add user on db
    # params = ('JohnDoe', 'pass#')
    # query = "INSERT INTO users (username, password) VALUES (%s, %s);"
    # db_session.execute(query, params)
    
    method = 'POST'
    body = json.dumps({'username': 'JohnDoe', 'password': 'pass#'})

    test_client.request(method, PATH_REGISTER, body, HEADERS)

    response = test_client.getresponse()

    assert response.status == 400


def test_user_login_route(test_client, user_on_db):
    user_on_db['user'] # add user on db
    
    method = 'POST'
    body = json.dumps({'username': 'JohnDoe', 'password': 'pass#'})

    test_client.request(method, PATH_LOGIN, body, HEADERS)

    response = test_client.getresponse()
    token = response.read().decode('utf-8')

    assert response.status == 200
    assert isinstance(token, str)


def test_user_login_route_invalid_username(test_client, user_on_db):
    user_on_db['user'] # add user on db
    
    method = 'POST'
    body = json.dumps({'username': 'invalid', 'password': 'pass#'})

    test_client.request(method, PATH_LOGIN, body, HEADERS)

    response = test_client.getresponse()

    assert response.status == 401


def test_user_login_route_invalid_password(test_client, user_on_db):
    user_on_db['user'] # add user on db
    
    method = 'POST'
    body = json.dumps({'username': 'JohnDoe', 'password': 'invalid'})

    test_client.request(method, PATH_LOGIN, body, HEADERS)

    response = test_client.getresponse()

    assert response.status == 401

