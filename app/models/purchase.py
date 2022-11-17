from flask import current_app as app


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
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, uid, address, order_time, quantity, fulfillment, fulfillment_time, price
FROM Orders
WHERE uid = :uid
ORDER BY order_time DESC
''',
                              seller_id=seller_id,)
        return [Purchase(*row) for row in rows]

