import pytest
import json
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])

PATH_ADD_CATEGORY= '/category/add'
PATH_LIST_CATEGORY= '/category/list'
PATH_DELETE_CATEGORY= '/category/delete'
HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer token'}


def test_add_category_route(test_client, db_session, clear_categories_db):
    method = 'POST'
    body = json.dumps({'name': 'Clothes', 'slug': 'clothes'})

    test_client.request(method, PATH_ADD_CATEGORY, body, HEADERS)

    response = test_client.getresponse()
    data = json.loads(response.read().decode('utf-8'))

    query = 'SELECT * FROM categories'
    categories_on_db = db_session.execute(query)

    assert response.status == 201
    assert categories_on_db[0][0] is not None # id
    assert data.get('data', None) == {
         "name": categories_on_db[0][1],
         "slug": categories_on_db[0][2],
     }


def test_list_categories_route(test_client, categories_on_db):
    method = 'GET'
    test_client.request(method=method, url=PATH_LIST_CATEGORY, headers=HEADERS)

    response = test_client.getresponse()
   
    data = json.loads(response.read().decode('utf-8'))
    categories = data.get('data', None)
    
    assert response.status == 200
    assert len(data) == 2
    assert categories[0] == {
        'id': categories_on_db[0]['id'],
        'name': categories_on_db[0]['name'],
        'slug': categories_on_db[0]['slug'],
     }


def test_delete_category_route(test_client, db_session, category_on_db):
    method = 'DELETE'
    _id = category_on_db[0]['id']
    url = f'{PATH_DELETE_CATEGORY}/{_id}'

    test_client.request(method=method, url=url, headers=HEADERS)

    response = test_client.getresponse()

    param = (_id,)
    query = 'SELECT * FROM categories WHERE id=%s'
    category_model = db_session.execute(query, param)

    assert response.status == 200
    assert not category_model
