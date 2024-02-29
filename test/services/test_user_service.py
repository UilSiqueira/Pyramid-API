import pytest
from decouple import config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from services.exceptions.exceptions import UserAlreadyExistsException, UserOrPasswordInvalidException

from services.user import UserService


crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

QUERY_USER = "INSERT INTO users (username, password) VALUES (%s, %s);"
QUERY_DELETE = 'DELETE FROM users'


def test_register_user(clear_users_db, db_session):
    _service = UserService(db_session)
    username = 'JohnDoe'
    password = 'pass#'

    _service.register_user(username, password)

    query = 'SELECT * FROM users'
    user_on_db = db_session.execute(query)

    assert user_on_db[0][1] == username
    assert crypt_context.verify(password, user_on_db[0][2])


def test_register_user_username_already_exists(db_session):
    username = 'JohnDoe'
    password = 'pass#'

    query = QUERY_USER
    values = (username, password)
    db_session.execute(query, values)

    _service = UserService(db_session)

    with pytest.raises(UserAlreadyExistsException):
        _service.register_user(username, password)


def test_user_login(db_session):
    username = 'JohnDoe'
    password = 'pass#'
    cript_password = crypt_context.hash('pass#')

    query = QUERY_USER
    values = (username, cript_password)
    db_session.execute(query, values)

    _service = UserService(db_session)

    token_data = _service.user_login(username=username, password=password)

    assert isinstance(token_data, str)


def teste_user_login_invalid_user(db_session):
    username = 'JohnDoeNotExists'
    password = 'pass#'

    _service = UserService(db_session)

    with pytest.raises(UserOrPasswordInvalidException):
        _service.user_login(username=username, password=password)
    

def test_user_login_invalid_password(db_session):
    username = 'JohnDoe'
    password = crypt_context.hash('pass#')
    invalid_password = 'invalid'

    query = QUERY_USER
    values = (username, password)
    db_session.execute(query, values)

    _service = UserService(db_session)

    with pytest.raises(UserOrPasswordInvalidException):
        _service.user_login(username=username, password=invalid_password)
    
    

def test_verify_token(db_session):
    username = 'JohnDoe'
    password = crypt_context.hash('pass#')
    
    query = QUERY_USER
    values = (username, password)
    db_session.execute(query, values)

    _service = UserService(db_session)

    data = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    _service.verify_token(token=access_token)
    

def test_verify_token_expired(db_session):
    username = 'JohnDoe'
    password = crypt_context.hash('pass#')
    
    query = QUERY_USER
    values = (username, password)
    db_session.execute(query, values)

    _service = UserService(db_session)

    data = {
        'sub': username,
        'exp': datetime.utcnow() - timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(UserOrPasswordInvalidException):
        _service.verify_token(token=access_token)