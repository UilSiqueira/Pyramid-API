import psycopg2
from decouple import config

TEST_MODE = config("TEST_MODE", default=False, cast=bool)

HOST = config('HOST_TEST') if TEST_MODE else config('HOST_PROD')
PORT = config('PORT')
DB = config('POSTGRES_DB')
USER = config('POSTGRES_USER')
PASSWORD = config('POSTGRES_PASSWORD')


class Session:
    def __init__(self, host=HOST, port=PORT, db= DB, user=USER, password=PASSWORD) -> None:
        self.db_config = {
            'host': host,
            'port': port,
            'database': db,
            'user': user,
            'password': password,
        }

    def execute(self, query, *params):
        connection = None
        result = True
        try:
            connection = psycopg2.connect(**self.db_config)
            with connection.cursor() as cursor:
                cursor.execute(query, *params)
                if cursor.description is not None:
                    result = cursor.fetchall()
                connection.commit()
        except Exception:
            if connection is not None:
                connection.rollback()
            result = None
            raise psycopg2.Error

        finally:
            if connection is not None:
                connection.close()

        return result