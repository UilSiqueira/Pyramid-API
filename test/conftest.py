import pytest
from core.db.connection import Session
import http.client
from decouple import config
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])


@pytest.fixture()
def db_session():
    session = Session()
    yield session


@pytest.fixture()
def test_client():
    host = config('HOST_CLIENT_TEST')
    port = config('HOST_CLIENT_PORT')
    
    try:
        conn = http.client.HTTPConnection(host, port)
        yield conn
    finally:
        conn.close()


@pytest.fixture()
def user_on_db(db_session):
    user = 'JohnDoe'
    cript_password = crypt_context.hash('pass#')
    params = (user, cript_password)
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    user = db_session.execute(query, params)

    yield {'user': user}


@pytest.fixture()
def categories_on_db(db_session):
    category_one = ('Clothes', 'clothes')
    category_two = ('Glasses', 'glasses')

    query = "INSERT INTO categories (name, slug) VALUES (%s, %s)"
    db_session.execute(query, category_one)
    db_session.execute(query, category_two)

    query = 'SELECT * FROM categories'
    categories_from_db = db_session.execute(query)

    categories = []
    for item in categories_from_db:
        _id, name, slug = item
        categories.append({'id': _id, 'name': name, 'slug': slug})

    yield categories


@pytest.fixture()
def category_on_db(db_session):
    params = ('Clothes', 'clothes')

    query = "INSERT INTO categories (name, slug) VALUES (%s, %s)"
    db_session.execute(query, params)

    query = 'SELECT * FROM categories'
    categories_from_db = db_session.execute(query)

    category = []
    for item in categories_from_db:
        _id, name, slug = item
        category.append({'id': _id, 'name': name, 'slug': slug})

    yield category


@pytest.fixture()
def product_on_db(db_session, categories_on_db):
    category_one = categories_on_db[0]
    category_two = categories_on_db[1]
 
    params_one = ('T-shirt', 't-shirt', 22.40, 10, category_one['id'])
    params_two = ('Sunglass', 'sunglass', 100.0, 5, category_two['id'])

    query = "INSERT INTO products (name, slug, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)"
    db_session.execute(query, params_one)
    db_session.execute(query, params_two)

    query = 'SELECT * FROM products'
    product_from_db = db_session.execute(query)

    products = []
    if product_from_db:
        for index, value in enumerate(product_from_db):
            _id, name, slug, price, stock, *_ = value
            products.append({'id': _id, 'name': name, 'slug': slug, 'price': price, 'stock': stock})
            products[index]['category'] = categories_on_db[index]
    yield products


@pytest.fixture(autouse=True)
def clear_users_db(db_session):
    db_session.execute('DELETE FROM users')
    yield db_session
    db_session.execute('DELETE FROM users')


@pytest.fixture(autouse=True)
def clear_categories_db(db_session):
    return db_session.execute('DELETE FROM categories')


@pytest.fixture(autouse=True)
def clear_products_db(db_session):
    db_session.execute('DELETE FROM products')
    db_session.execute('DELETE FROM categories')
    yield db_session
    db_session.execute('DELETE FROM products')
    db_session.execute('DELETE FROM categories')




