from flask import current_app as app, flash


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
SELECT uid, product_id
FROM Carts
WHERE uid = :uid
AND time_added_to_cart >= :since
ORDER BY time_added_to_cart DESC
''',
                              uid=uid,
                              since=since)
        return [Cart(*row) for row in rows]
    
  #  @staticmethod
  #  def get_items_in_cart_by_uid(uid):
  #      rows = app.db.execute('''
#SELECT uid, product_id, quantity
#FROM Carts
#WHERE uid = :uid
 #       ''', uid = uid)
  #      return [Cart(*row) for row in rows]
        
class UserCart:
    def __init__(self, product_name, quantity, price):
        self.product_name = product_name,
        self.quantity = quantity
        self.price = price
    
    @staticmethod
    def get_items_in_cart_by_uid(uid):
        rows = app.db.execute('''
SELECT products.product_name, carts.quantity, products.price
FROM Carts, Products
WHERE uid = :uid
  AND carts.product_id = products.product_id
''',
        uid = uid)
        return [UserCart(*row) for row in rows]

    def add_item_to_cart(uid, product_id, quantity): #Will add functionality to choose quantity/update outstanding orders later
        try:
            rows = app.db.execute("""
INSERT INTO Carts(uid, product_id, quantity)
VALUES(:uid, :product_id, :quantity)
""",
                                uid = uid,
                                product_id = product_id,
                                quantity = quantity)
        except Exception as e:
            print("Failed to add to cart")
        #flash("Item Added")
        return None