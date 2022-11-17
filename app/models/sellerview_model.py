from flask import current_app as app

class Product:
    def __init__(self, uid, seller):
        self.product_id = product_id,
        self.seller_id = seller_id,
        self.product_name = product_name,
        self.category = category,
        self.description = description,
        self.image = image,
        self.price = price,
        self.available = available,
        self.quantity = quantity


    def addProducts(product_id, seller_id, product_name, category, description, image, price, available, quantity):
        app.db.execute("""
INSERT INTO Products
VALUES (product_id, seller_id, product_name, category, description, image, price, available, quantity)
""",
                              product_id = product_id, seller_id = seller_id, product_name, category = category, description = description, image = image, price = price, available = available, quantity = quantity)
        
        return 1
    
    def removeProducts(uid, product_name):
        app.db.execute("""
DELETE FROM Products
WHERE uid = :uid AND product_name = product_name
""",
                              uid = uid, product_name=product_name)
        
        return 1
