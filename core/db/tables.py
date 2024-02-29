USER = (
            'CREATE TABLE IF NOT EXISTS users ('
            'id SERIAL PRIMARY KEY,'
            'username VARCHAR NOT NULL unique,'
            'password VARCHAR NOT NULL,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
        )

PRODUCT = (
            'CREATE TABLE IF NOT EXISTS products ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR NOT NULL,'
            'slug VARCHAR NOT NULL,'
            'price FLOAT,'
            'stock INTEGER,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'category_id INTEGER NOT NULL,'
            'FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE);'
        )


CATEGORY = (
            'CREATE TABLE IF NOT EXISTS categories ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR NOT NULL,'
            'slug VARCHAR NOT NULL);'
        )