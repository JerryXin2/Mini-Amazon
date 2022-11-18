from flask import current_app as app
from random import randint


class Product:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.description = description
        self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id
AND available = :available
''',
                              seller_id=seller_id,
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_products(k, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''',
                              k = k,
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def search_products(search_key, available=True):
        rows = app.db.execute('''
    SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
    FROM Products
    WHERE product_name LIKE CONCAT('%', :search_key, '%')
    GROUP BY product_id, category
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def search_product_descriptions(search_key, available=True):
        rows = app.db.execute('''
    SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
    FROM Products
    WHERE description LIKE CONCAT('%', :search_key, '%')
    GROUP BY product_id, category
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def sort_price_asc(search_key, available=True):
        rows = app.db.execute('''
    SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
    FROM Products
    WHERE product_name LIKE CONCAT('%', :search_key, '%')
    GROUP BY product_id, category
    ORDER BY price ASC
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def sort_price_desc(search_key, available=True):
        rows = app.db.execute('''
    SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
    FROM Products
    WHERE product_name LIKE CONCAT('%', :search_key, '%')
    GROUP BY product_id, category
    ORDER BY price DESC
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def specific_prod(prod_id, available=True):
        rows = app.db.execute('''
    SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
    FROM Products
    WHERE product_id = :prod_id
    ''',
                                prod_id = prod_id,
                                available=available)
        return [Product(*row) for row in rows]

    def addProducts(seller_id, product_name, category, description, image,  price, available, quantity):
        app.db.execute("""
INSERT INTO Products
VALUES (:product_id, :seller_id, :product_name, :category, :description, :image, :price, :available, :quantity)
""",
                              product_id = randint(0, 240000000), seller_id = seller_id, product_name = product_name, category = category, description = description, image = 0, price = price, available = available, quantity = quantity)
        
        return 1
    
    def removeProducts(uid, product_name):
        app.db.execute("""
DELETE FROM Products
WHERE seller_id = :uid AND product_name = :product_name
""",
                              uid = uid, product_name=product_name)
        
        return 1
    
    @staticmethod
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products
WHERE seller_id = :seller_id
''',
                              seller_id = seller_id)
        return [Product(*row) for row in rows]



