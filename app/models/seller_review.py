from flask import current_app as app


#CREATE TABLE Seller_Reviews(
#    seller_id INT NOT NULL REFERENCES Sellers(uid),
#    reviewer_id INT NOT NULL REFERENCES Users(uid),
#    review VARCHAR(65535) NOT NULL,
#    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#    rating INT NOT NULL,
#    PRIMARY KEY(reviewer_id, seller_id)
#);
class Seller_Review:
    def __init__(self, seller_id, reviewer_id, review, review_time, rating):
        self.seller_id = seller_id
        self.reviewer_id = reviewer_id
        self.review = review
        self.review_time = review_time
        self.rating = rating

    @staticmethod
    def addSellerReview(seller_id, reviewer_id, review, review_time, rating):
        app.db.execute("""
    INSERT INTO Seller_Reviews(seller_id, reviewer_id, review, review_time, rating)
    VALUES(:seller_id, :reviewer_id, :review, :review_time, :rating)
    """,
                                seller_id = seller_id, reviewer_id=reviewer_id, review=review, review_time = review_time, rating = rating)
            
        return 1

