from models.base_model import BaseModel
from passlib.context import CryptContext
crypt_context = CryptContext(schemes=['sha256_crypt'])


class User(BaseModel):

    def add(self, username: str, password: str):
        crypt_password = crypt_context.hash(password)
        params = (username, crypt_password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s);"

        self.db_session.execute(query, params)

    def list(self, user: str = ''):
        username = (user, )
        query = 'SELECT * FROM users;'
        if user:
            query = "SELECT username, password FROM users WHERE username=%s;"
        user_on_db = self.db_session.execute(query, username)
        if user_on_db:
            return user_on_db[0]
        return None
