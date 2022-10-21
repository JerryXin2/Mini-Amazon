from flask import current_app as app


#   product_id INT NOT NULL REFERENCES Products(product_id),
#    uid INT NOT NULL REFERENCES Users(uid),
#    review VARCHAR(65535) NOT NULL,
#    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#    PRIMARY KEY(uid, product_id)
class Product_Review:
    def __init__(self, product_id, uid, review, review_time):
        self.product_id = product_id
        self.uid = uid
        self.review = review
        self.review_time = review_time

    @staticmethod
    def get(product_id, uid):
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time
FROM Product_Reviews
WHERE product_id = :product_id AND uid = :uid
''',
                              product_id=product_id, 
                              uid=uid)
        return Product_Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time
FROM Product_Reviews
''',
                              )
        return [Product_Review(*row) for row in rows]

    @staticmethod
    def get_recent_reviews(uid):
        rows = app.db.execute('''
SELECT product_id, uid, review, review_time
FROM Product_Reviews
WHERE uid = :uid
ORDER BY review_time DESC
LIMIT 5
''',
                              uid=uid)
        return [Product_Review(*row) for row in rows]

