from flask import current_app as app


class Purchase:
    def __init__(self, product_id, seller_id, uid, address, order_time, quantity, fulfillment):
        self.product_id = product_id
        self.seller_id = seller_id
        self.uid = uid
        self.address = address
        self.order_time = order_time
        self.quantity = quantity
        self.fulfillment = fulfillment

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, seller_id, uid, address, order_time, quantity, fulfillment
FROM Orders
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT product_id, seller_id, uid, address, order_time, quantity, fulfillment
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
SELECT product_id, seller_id, uid, address, order_time, quantity, fulfillment
FROM Orders
WHERE uid = :uid
ORDER BY order_time DESC
''',
                              uid=uid,)
        return [Purchase(*row) for row in rows]

