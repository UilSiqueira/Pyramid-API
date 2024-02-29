import pytest
from services.product import ProductService
from pyramid.httpexceptions import HTTPNotFound

def test_add_product_service(db_session, category_on_db, clear_products_db):
    product = {
        'category_slug': category_on_db[0]['slug'],
        'product': {
            'name': 'Clothes',
            'slug': 'clothes1',
            'price': 22.40,
            'stock': 10
        }
    }
    _service = ProductService(db_session)

    _service.add_product(**product)

    query = 'SELECT * FROM products'
    product_from_db = db_session.execute(query)

    assert len(product_from_db) == 1
    assert product_from_db[0][1] == product['product']['name']
    assert product_from_db[0][2] == product['product']['slug']
    assert product_from_db[0][3] == product['product']['price']
    assert product_from_db[0][4] == product['product']['stock']


def test_add_product_service_invalid_category(clear_products_db, db_session, product_on_db, category_on_db):
    product = {
        'category_slug': 'invalid',
        'product': {
            'name': 'Clothes',
            'slug': 'clothes',
            'price': 22.40,
            'stock': 10
        }
    }

    _service = ProductService(db_session)

    with pytest.raises(HTTPNotFound):
        _service.add_product(**product)


def test_update_product(db_session, product_on_db):

    product = {
        'name': 'T-shirt',
        'slug': 't-shirt',
        'price': 20.00,
        'stock': 50
    }
    _id = product_on_db[0]['id']
    _service = ProductService(db_session)
    _service.update_product(id=_id, **product)

    query = 'SELECT * FROM products WHERE id=%s'
    params = (_id, )
    product_from_db = db_session.execute(query, params)
    _, name, slug, price, stock, *_ = product_from_db[0]

    assert product_from_db is not None
    assert name == product['name']
    assert slug == product['slug']
    assert price == product['price']
    assert stock == product['stock']


def test_update_product_invalid_id(db_session, product_on_db):
    product = {
        'name': 'T-shirt',
        'slug': 't-shirt',
        'price': 20.00,
        'stock': 50
    }
    _id = product_on_db[0]['id']
    _service = ProductService(db_session)
   

    with pytest.raises(HTTPNotFound):
         _service.update_product(id=100000, **product)


def test_delete_product(db_session, product_on_db):
    _id = product_on_db[0]['id']
    _service = ProductService(db_session)
    _service.delete_product(id=product_on_db[0]['id'])

    query = 'SELECT * FROM products WHERE id=%s'
    params = (_id, )
    product_from_db = db_session.execute(query, params)

    assert len(product_from_db) == 0


def test_delete_product_non_exist(db_session):
    _service = ProductService(db_session)
    
    with pytest.raises(HTTPNotFound):
        _service.delete_product(id=1000)


def test_list_product_service(db_session, product_on_db):
    _service = ProductService(db_session)

    product = _service.list_products(search='')

    assert product_on_db[0] == product[0]
    assert product_on_db[1] == product[1]


def test_list_products_with_search(db_session, product_on_db):
    _service = ProductService(db_session)

    product = _service.list_products(search='T-shirt')

    assert len(product) == 1
    assert product[0]['name'] == product_on_db[0]['name']
    assert product[0]['category']['name'] == product_on_db[0]['category']['name']
