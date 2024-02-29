import pytest
import json
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])

PATH_ADD_PRODUCT= '/product/add'
PATH_LIST_PRODUCT= '/product/list'
PATH_DELETE_PRODUCT= '/product/delete'
PATH_UPDATE_PRODUCT = '/product/update'
HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer token'}


def test_add_product_route(test_client, categories_on_db):
    method = 'POST'
    body = json.dumps({
        'category_slug': categories_on_db[0]['slug'],
        'product': {
            'name': 'Clothes',
            'slug': 'clothes',
            'price': 22.40,
            'stock': 10
        }, 
    })
    test_client.request(method, PATH_ADD_PRODUCT, body, HEADERS)
    response = test_client.getresponse()

    assert response.status == 201


def test_add_product_route_invalid_category_slug(test_client, categories_on_db):
    method = 'POST'
    body = json.dumps({
        'category_slug': 'invalid',
        'product': {
            'name': 'Clothes',
            'slug': 'clothes',
            'price': 22.40,
            'stock': 10
        },
    })
    test_client.request(method, PATH_ADD_PRODUCT, body, HEADERS)
    response = test_client.getresponse()

    assert response.status == 404


def test_update_product_route(test_client, db_session, product_on_db):
    method = 'PUT'
    product = {
        "name": "Updated T-shirt",
        "slug": "updated-tshirt",
        "price": 23.88,
        "stock": 10
    }
    body = json.dumps(product)
    
    test_client.request(method, f'{PATH_UPDATE_PRODUCT}/{product_on_db[0]["id"]}', body, HEADERS)
    response = test_client.getresponse()

    query = 'SELECT * FROM products WHERE id=%s'
    param = (product_on_db[0]["id"], )
    product_from_db = db_session.execute(query, param)
    
    assert response.status == 200
    assert product_from_db[0][1] == product['name']
    assert product_from_db[0][2] == product['slug']
    assert product_from_db[0][3] == product['price']
    assert product_from_db[0][4] == product['stock']


def test_update_product_route_invalid_id(test_client, product_on_db):
    method = 'PUT'
    body = json.dumps({
        "name": 'Updated T-shirt',
        "slug": 'updated-tshirt',
        "price": 23.88,
        "stock": 10
    })

    test_client.request(method, f'{PATH_UPDATE_PRODUCT}/{1000}', body, HEADERS)
    response = test_client.getresponse()
    
    assert response.status == 404


def test_delete_product(test_client, db_session, product_on_db):
    method = 'DELETE'
    path = f'{PATH_DELETE_PRODUCT}/{product_on_db[0]["id"]}'
    
    test_client.request(method=method, url=path, headers=HEADERS)
    response = test_client.getresponse()

    query = 'SELECT * FROM products WHERE id=%s'
    param = (product_on_db[0]["id"], )
    product_from_db = db_session.execute(query, param)
    
    assert response.status == 200
    assert not product_from_db


def test_delete_product_non_exist(test_client, product_on_db):
    method = 'DELETE'
    path = f'{PATH_DELETE_PRODUCT}/{1000}'
    
    test_client.request(method=method, url=path, headers=HEADERS)
    response = test_client.getresponse()

    assert response.status == 404
