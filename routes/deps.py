
from decouple import config
from core.db.connection import Session
from services.user import UserService
from pyramid.response import Response
from functools import wraps

TEST_MODE = config('TEST_MODE', default=False, cast=bool)


def require_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        authorization_header = request.headers.get("Authorization", "")

        if authorization_header and authorization_header.startswith("Bearer "):
            token = authorization_header.split(" ")[1]

            if TEST_MODE:
                return view_func(request, *args, **kwargs)

            session = Session()
            user = UserService(db_session=session)
            user.verify_token(token=token)

            return view_func(request, *args, **kwargs)
        else:
            return Response('Token not valid', status_code=401)

    return wrapper
