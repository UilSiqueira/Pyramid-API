from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from core.db.create_tabels import create_tables
from routes.category import add_category_route, list_category_route, delete_category_route
from routes.product import add_product_route, list_product_route, update_product_route, delete_product_route
from routes.user import user_register, user_login


def App():
    create_tables()
    with Configurator() as config:
        # category
        config.add_route('category_add', '/category/add')
        config.add_view(add_category_route, route_name='category_add', request_method='POST', renderer='json')
        config.add_route('category_list', '/category/list')
        config.add_view(list_category_route, route_name='category_list', request_method='GET', renderer='json')
        config.add_route('category_delete', '/category/delete/{id}')
        config.add_view(delete_category_route, route_name='category_delete', request_method='DELETE', renderer='json')
        # product
        config.add_route('product_add', '/product/add')
        config.add_view(add_product_route, route_name='product_add', request_method='POST', renderer='json')
        config.add_route('product_list', '/product/list')
        config.add_view(list_product_route, route_name='product_list', request_method='GET', renderer='json')
        config.add_route('product_update', '/product/update/{id}')
        config.add_view(update_product_route, route_name='product_update', request_method='PUT', renderer='json')
        config.add_route('product_delete', '/product/delete/{id}')
        config.add_view(delete_product_route, route_name='product_delete', request_method='DELETE', renderer='json')
        # user
        config.add_route('user_register', '/user/register')
        config.add_view(user_register, route_name='user_register', request_method='POST', renderer='json')
        config.add_route('user_login', '/user/login')
        config.add_view(user_login, route_name='user_login', request_method='POST', renderer='json')

        config.scan()

    return config.make_wsgi_app()

if __name__ == '__main__':
    app = App()
    server = make_server('0.0.0.0', 6543, app)
    print(server)
    server.serve_forever()