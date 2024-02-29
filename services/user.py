from decouple import config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

from services.exceptions.exceptions import UserOrPasswordInvalidException, UserAlreadyExistsException
from models.user import User as UserModel
from core.db.connection import Session

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


class UserService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    def register_user(self, username: str, password: str):
        user = UserModel(self.db_session)
        try:
            user.add(username, password)
        except Exception:
            raise UserAlreadyExistsException('Username already exists')
        
    def user_login(self, username: str, password: str):
        expires_in = 30
        user_on_db = self._get_user(username)

        if not user_on_db:
            raise UserOrPasswordInvalidException('Username or password does not exists')
        
        if not crypt_context.verify(password, user_on_db[1]):
            raise UserOrPasswordInvalidException('Username or password does not exists')
        
        expires_at = datetime.utcnow() + timedelta(expires_in)
        data = {
            'sub': user_on_db[0],
            'exp': expires_at
        }
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return access_token

    def verify_token(self, token: str):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise UserOrPasswordInvalidException
        
        user_on_db = self._get_user(user=data['sub'])

        if user_on_db is None:
            raise UserOrPasswordInvalidException

    def _get_user(self, user: str):
        username = UserModel(self.db_session)
        user_on_db = username.list(user)

        if user_on_db:
            return user_on_db
        return None
