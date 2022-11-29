from flask import current_app as app

from app.models.product import Product


class Purchase:
    def __init__(self, order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price):
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.uid = uid
        self.address = address
        self.order_time = order_time
        self.quantity = quantity
        self.fulfillment = fulfillment
        self.fulfillment_time = fulfillment_time
        self.price = price

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price
FROM Orders
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price
FROM Orders
WHERE uid = :uid
AND order_time >= :since
ORDER BY order_time DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price
FROM Orders
WHERE uid = :uid
ORDER BY order_time DESC
''',
                              uid=uid,)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_fulfillment_status(seller_id):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price
FROM Orders
WHERE seller_id = :seller_id AND fulfillment = FALSE
ORDER BY order_time DESC
''',
                              seller_id=seller_id)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_most_recent(uid, search_key):
        rows = app.db.execute('''
SELECT order_id, Orders.product_id, Orders.seller_id, uid, address, order_time, Orders.quantity, fulfillment, fulfillment_time, Orders.price
FROM Orders, Products
WHERE Orders. uid = :uid and Orders.product_id  = Products.product_id and Products.product_name LIKE CONCAT('%', :search_key, '%')
ORDER BY order_time DESC
''',
                              uid=uid, search_key =search_key)
        return [Purchase(*row) for row in rows]

    def get_all_by_uid_price_asc(uid, search_key):
        rows = app.db.execute('''
SELECT order_id, Orders.product_id, Orders.seller_id, uid, address, order_time, Orders.quantity, fulfillment, fulfillment_time, Orders.price
FROM Orders, Products
WHERE Orders. uid = :uid and Orders.product_id  = Products.product_id and Products.product_name LIKE CONCAT('%', :search_key, '%')
ORDER BY price ASC
''',
                              uid=uid, search_key =search_key)
        return [Purchase(*row) for row in rows]

    def get_all_by_uid_price_desc(uid, search_key):
        rows = app.db.execute('''
SELECT order_id, Orders.product_id, Orders.seller_id, uid, address, order_time, Orders.quantity, fulfillment, fulfillment_time, Orders.price
FROM Orders, Products
WHERE Orders. uid = :uid and Orders.product_id  = Products.product_id and Products.product_name LIKE CONCAT('%', :search_key, '%')
ORDER BY price DESC
''',
                              uid=uid, search_key =search_key)
        return [Purchase(*row) for row in rows]

    def removeProductsbyFulfillmentStatus(uid, product_name):
        app.db.execute("""
UPDATE Orders
SET fulfillment = TRUE
WHERE product_name = :product_name;
""",
                              uid = uid, product_name=product_name)
        
        return 1

