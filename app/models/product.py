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
        self.review = review
        self.seller = seller



    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.product_id = :product_id 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.available = :available 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(seller_id, available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.seller_id = :seller_id 
AND p.product_id = pr.product_id
AND p.available = :available
AND p.seller_id = s.uid
''',
                              seller_id=seller_id,
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_products(k, available=True):
        rows = app.db.execute('''
SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
FROM Products as p, Product_Reviews as pr, Sellers as s
WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
AND p.product_id = pr.product_id
AND p.seller_id = s.uid
ORDER BY p.price DESC
LIMIT :k
''',
                              k = k,
                              available=available)
        return [Product(*row) for row in rows]

    
    
    
    @staticmethod
    def search_related_products(prod_name, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', SUBSTRING(:prod_name, 0, 5), '%') 
    AND p.product_id = pr.product_id 
    AND p.seller_id = s.uid
    AND p.product_name != :prod_name
    GROUP BY p.product_id, p.category, pr.review, s.seller
    ''',
                                prod_name = prod_name,
                                available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def search_product_descriptions(search_key, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.description LIKE CONCAT('%', :search_key, '%')
    AND p.seller_id = s.uid
    GROUP BY p.product_id, p.category, pr.review, s.seller
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def sort_price_asc(search_key, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    GROUP BY p.product_id, p.category, pr.rating, s.seller
    ORDER BY p.price ASC
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def sort_price_desc(search_key, available=True):
        rows = app.db.execute('''
    SELECT DISTINCT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    GROUP BY p.product_id, p.category, pr.rating, pr.review, s.seller
    ORDER BY p.price DESC
    ''',
                                search_key = search_key,
                                available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def specific_prod(prod_id, available=True):
        rows = app.db.execute('''
    SELECT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_id = pr.product_id AND p.product_id = :prod_id 
    AND p.seller_id = s.uid
    ''',
                                prod_id = prod_id,
                                available=available)
        return [Product(*row) for row in rows]

    def addProducts(product_id, seller_id, product_name, category, description, image,  price, available, quantity):
        app.db.execute("""
INSERT INTO Products
VALUES (:product_id, :seller_id, :product_name, :category, :description, :image, :price, :available, :quantity)
""",
                              product_id = product_id, seller_id = seller_id, product_name = product_name, category = category, description = description, image = 0, price = price, available = available, quantity = quantity)
        
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
SELECT DISTINCT product_id, product_name, category, description, image, price, available, seller_id, quantity
FROM Products as p
WHERE seller_id = :seller_id
''',
                              seller_id = seller_id)
        return [Product(*row) for row in rows]

    @staticmethod
    def filter_category(search_key, cat, sortPrice, available=True):
        if sortPrice == 'High to Low':
            order_by1 = 'ORDER BY price DESC'
        if sortPrice == 'Low to High':
            order_by1 = 'ORDER BY price'
        if sortPrice == 'None':
            order_by1 = ''

        SQL_str ='''SELECT DISTINCT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, pr.rating, pr.review, s.seller
                    FROM Products as p, Product_Reviews as pr, Sellers as s
                    WHERE p.product_id = pr.product_id AND p.product_id = :prod_id 
                        AND p.category = :cat
                        AND p.seller_id = s.uid
                    '''
        SQL_str = SQL_str + '\n' + order_by1
        rows = app.db.execute(SQL_str,
                              search_key = search_key,
                              available=available,
                              sortPrice = sortPrice,
                              cat = cat
                              )
        return [Product(*row) for row in rows]



class P1:
    def __init__(self, product_id, product_name, category, description, image, price, available, seller_id, quantity, rating, seller):
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

    @staticmethod
    def search_products(search_key, available=True):
        rows = app.db.execute('''
    SELECT DISTINCT p.product_id, p.product_name, p.category, p.description, p.image, p.price, p.available, p.seller_id, p.quantity, AVG(pr.rating) as avg_rating, s.seller
    FROM Products as p, Product_Reviews as pr, Sellers as s
    WHERE p.product_name LIKE CONCAT('%', :search_key, '%') 
    AND p.product_id = pr.product_id
    AND p.seller_id = s.uid
    GROUP BY p.product_id, p.category, s.seller
    ''',
                                search_key = search_key,
                                available=available)
        return [P1(*row) for row in rows]