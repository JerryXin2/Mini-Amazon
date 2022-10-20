from flask import current_app as app


class Cart:
    def __init__(self, uid, product_id, quantity):
        self.uid = uid
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, product_id, quantity
FROM Carts
WHERE uid = :uid
''',
                              uid= uid)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, product_id, time_added_to_cart
FROM Carts
WHERE uid = :uid
AND time_added_to_cart >= :since
ORDER BY time_added_to_cart DESC
''',
                              uid=uid,
                              since=since)
        return [Cart(*row) for row in rows]
    
    @staticmethod
    def get_items_in_cart_by_uid(uid):
        rows = app.db.execute('''
SELECT product_id, quantity
FROM Carts
WHERE uid = :uid
        ''', uid = uid)
        return [Cart(*row) for row in rows]
