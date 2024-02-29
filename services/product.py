from models.product import Product as ProducModel
from core.db.connection import Session
from typing import Dict


class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._product_model = ProducModel(db_session)

    def add_product(self, product: Dict, category_slug: str):
        self._product_model.add(product, category_slug)

    def list_products(self, search: str = ''):
        products = []
        products_from_db = self._product_model.list(search)
        
        if products_from_db:
            products = [self.serialize_product(product) for product in products_from_db]

        return products

    def update_product(self, id: int, name: str, slug: str, price: float, stock: str):
        self._product_model.update(id, name, slug, price, stock)

    def delete_product(self, id):
        self._product_model.delete(id)
    
    def serialize_product(self, product_from_db: tuple):
        product = {}
        _id, nome, slug, price, stock, _, _, category_id = product_from_db
        product = {'id': _id, 'name': nome, 'slug': slug, 'price': price, 'stock': stock}

        query = 'SELECT * FROM categories WHERE id=%s;'
        params = (category_id, )
        categories_from_db = self.db_session.execute(query, params)

        category = {}
        _id, nome, slug = categories_from_db[0]
        category = {'id': _id, 'name': nome, 'slug': slug}
        product['category'] = category
        return product

