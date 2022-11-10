from random import randint
from flask_login import UserMixin, current_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class Seller:
    def __init__(self, uid, seller):
        self.uid = uid
        self.seller = seller
    
    def register(uid,seller):
        try:
            rows = app.db.execute("""
INSERT INTO Sellers(uid, seller)
VALUES(:uid, :seller)
RETURNING uid
""",
                                  uid = uid, seller = seller)
            uid = rows[0][0]
            return 1
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


