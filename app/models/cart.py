from flask import current_app as app


class Cart:
    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get(cart_id):
        rows = app.db.execute('''
SELECT cart_id, product_id, quantity
FROM Carts
WHERE cart_id = :cart_id
''',
                              cart_id= cart_id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(cart_id, since):
        rows = app.db.execute('''
SELECT cart_id, product_id, time_added_to_cart
FROM Carts
WHERE cart_id = :cart_id
AND time_added_to_cart >= :since
ORDER BY time_added_to_cart DESC
''',
                              cart_id=cart_id,
                              since=since)
        return [Cart(*row) for row in rows]
    
    @staticmethod
    def get_items_in_cart_by_uid(cart_id):
        rows = app.db.execute('''
SELECT product_id, quantity
FROM Carts
WHERE cart_id = :cart_id
        ''', cart_id = cart_id)
        return [Cart(*row) for row in rows]
