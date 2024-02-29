from models.base_model import BaseModel


class Category(BaseModel):

    def add(self, name: str, slug: str):
        params = (name, slug)
        query = "INSERT INTO categories (name, slug) VALUES (%s, %s);"
        self.db_session.execute(query, params)

    def list(self, id: str = ''):
        categories = []
        param = (id, )
        query = 'SELECT * FROM categories;'
        if id:
            query = 'SELECT * FROM categories WHERE id=%s;'
        categories_from_db = self.db_session.execute(query, param)
        if categories_from_db:
            categories = self._to_dict(categories_from_db)
        return categories
    
    def delete(self, id: str):
        param = (id, )
        query = 'DELETE FROM categories WHERE id=%s;'

        self.db_session.execute(query, param)
    
    def _to_dict(self, data_from_db):
        categories = []
        for item in data_from_db:
            _id, nome, slug = item
            categories.append({'id': _id, 'name': nome, 'slug': slug})
        return categories