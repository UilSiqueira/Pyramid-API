
from core.db.connection import Session
from services.category import CategoryService
from routes.deps import require_auth
from pyramid.response import Response


@require_auth
def add_category_route(request):
    session = Session()
    category = CategoryService(session)
    
    payload = request.json_body
    category.add_category(**payload)
    response = Response(
        status='201 Created',
        json_body={
            'message': 'Created successfully',
            'data': payload,
        }
    )
    return response


@require_auth
def list_category_route(request):
    session = Session()
    category = CategoryService(session)
    
    categories = category.list_categories()
    response = Response(
        status='200 Success',
        json_body={
            'message': 'Operation successful',
            'data': categories,
        }
    )
    return response


@require_auth
def delete_category_route(request):
    session = Session()
    category = CategoryService(session)

    id_param = request.matchdict.get('id')
    category.delete_category(id=id_param)

    response = Response(
        status='200 Success',
    )
    return response
