from models.base_model import BaseModel
from typing import Dict
from pyramid.httpexceptions import HTTPNotFound


class Product(BaseModel):

    def add(self, product: Dict, category_slug: str):
        query_category = 'SELECT * FROM categories WHERE slug=%s;'
        params_category = (category_slug, )
        category = self.db_session.execute(query_category, params_category)
        if not category:
            raise HTTPNotFound(f'No category was found with slug {category_slug};')
        
        category_id = category[0][0]
        name, slug, price, stock = product.values()
        query_product = 'INSERT INTO products (name, slug, price, stock, category_id) VALUES (%s, %s, %s, %s, %s);'
        params_product = (name, slug, price, stock, category_id)

        self.db_session.execute(query_product, params_product)

    def list(self, search: str = ''):
        if search:
            query = 'SELECT * FROM products WHERE name ILIKE %s OR slug ILIKE %s;'
            params = (search, search)
            products_from_db = self.db_session.execute(query, params)
            return products_from_db
        
        query = 'SELECT * FROM products;'
        products_from_db = self.db_session.execute(query)
        return products_from_db
    
    def update(self, id: int, name: str, slug: str, price: float, stock: str):
        params_product = (id, )
        query_product = 'SELECT * FROM products WHERE id=%s;'
        product = self.db_session.execute(query_product, params_product)
        if not product:
            raise HTTPNotFound(f"No product found with id {id};")
        
        query = "UPDATE products SET name = %s, slug = %s, price = %s, stock = %s WHERE id = %s;"
        params = (name, slug, price, stock, id)
        
        self.db_session.execute(query, params)

    def delete(self, id: str):
        query_product = 'SELECT * FROM products WHERE id=%s;'
        params_product = (id, )
        product = self.db_session.execute(query_product, params_product)
        if not product:
            raise HTTPNotFound(f'No product found with id {id};')
        
        query = 'DELETE FROM products WHERE id=%s;'
        params = (id, )
        self.db_session.execute(query, params)

    def _to_dict(self, data_from_db):
        categories = []
        for item in data_from_db:
            _id, nome, slug = item
            categories.append({'id': _id, 'name': nome, 'slug': slug})
        return categories
