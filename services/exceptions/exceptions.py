from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPUnauthorized


class UserAlreadyExistsException(HTTPBadRequest):
    def __init__(self, message="User already exists"):
        super().__init__(json_body={'error': 'user_already_exists', 'message': message})


class UserOrPasswordInvalidException(HTTPUnauthorized):
    def __init__(self, message="Username or password does not exists"):
        super().__init__(json_body={'error': 'invalid_input', 'message': message})
