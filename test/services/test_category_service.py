import pytest
from services.category import CategoryService
from models.category import Category as CategoryModel
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest


def test_add_category_service(db_session, clear_categories_db, ):

    _service = CategoryService(db_session)

    _service.add_category(name='Clothes', slug='clothes')

    query = "SELECT * FROM categories"
    categories_on_db = db_session.execute(query)

    query = "DELETE FROM categories"
    db_session.execute(query)

    assert len(categories_on_db) == 1
 
    assert categories_on_db[0][1] == 'Clothes'
    assert categories_on_db[0][2] == 'clothes'


def test_list_category_service(db_session, categories_on_db):

    _service = CategoryService(db_session)

    categories = _service.list_categories()

    assert len(categories) == 2
 
    assert categories[0]['id'] == categories_on_db[0]['id']
    assert categories[0]['name'] == categories_on_db[0]['name']
    assert categories[0]['slug'] == categories_on_db[0]['slug']

def test_delete_category_service(db_session, category_on_db):

    _service = CategoryService(db_session)

    _service.delete_category(category_on_db[0]['id'])

    query = "SELECT * FROM categories"
    categories = db_session.execute(query)

    assert not categories
