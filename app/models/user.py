from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname, address, password, balance):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.password = password
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(uid, email, firstname, lastname, address, password, balance)
VALUES(uid, email, firstname, lastname, address, password, 0)
RETURNING uid
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address = address)
            uid = rows[0][0]
            return User.get(uid)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, address, password, balance
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None
