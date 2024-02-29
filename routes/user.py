from core.db.connection import Session
from services.user import UserService

from pyramid.response import Response
from services.exceptions.exceptions import UserOrPasswordInvalidException, UserAlreadyExistsException
from pyramid.httpexceptions import HTTPBadRequest

def user_register(request):
    session = Session()
    user = UserService(session)
    payload = request.json_body
    user.register_user(**payload)
    response = Response(
        status='201 Created',
        json_body={
            'message': 'User Created successfully',
            'data': payload,
        })

    return response


def user_login(request):
    session = Session()
    user = UserService(session)
    payload = request.json_body
    token_data = user.user_login(**payload)
    return token_data