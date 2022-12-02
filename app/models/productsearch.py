from flask import current_app as app

class Product:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity, rating, review, seller):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.description = description
        self.image = image
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.quantity = quantity
        self.rating = rating
        self.percentage = (rating/5)*100
        self.seller = seller