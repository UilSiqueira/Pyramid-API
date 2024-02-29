from pyramid.response import Response

from core.db.connection import Session
from services.product import ProductService
from routes.deps import require_auth

HTTP_200_SUCCESS = '200 Success'
HTTP_201_CREATED = '201 Created'


@require_auth
def add_product_route(request):
    session = Session()
    product = ProductService(session)
    
    payload = request.json_body
    product.add_product(**payload)
    response = Response(
        status=HTTP_201_CREATED,
        json_body={
            'message': 'Created successfully',
            'data': payload,
        }
    )
    return response


@require_auth
def list_product_route(request):
    session = Session()
    product = ProductService(session)
    
    products = product.list_products()
    response = Response(
        status=HTTP_200_SUCCESS,
        json_body={
            'message': 'Operation successful',
            'data': products,
        }
    )
    return response


@require_auth
def update_product_route(request):
    session = Session()
    product = ProductService(session)
    payload = request.json_body

    id_param = request.matchdict.get('id')
    product.update_product(id=id_param, **payload)

    response = Response(
        status=HTTP_200_SUCCESS,
    )
    return response


@require_auth
def delete_product_route(request):
    session = Session()
    product = ProductService(session)

    id_param = request.matchdict.get('id')
    product.delete_product(id=id_param)

    response = Response(
        status=HTTP_200_SUCCESS,
    )
    return response
