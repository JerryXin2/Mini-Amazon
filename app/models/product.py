from flask import current_app as app


class Product:
    def __init__(self, product_id, product_name, price, available, seller_id):
        self.product_id = product_id
        self.product_name = product_name
        #self.category = category
        #self.description = description
        #self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, product_name, price, available, seller_id
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, price, available, seller_id
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id, available=True):
        rows = app.db.execute('''
SELECT product_id, product_name, price, available, seller_id
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
SELECT product_id, product_name, price, available, seller_id
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''',
                              k = k,
                              available=available)
        return [Product(*row) for row in rows]

