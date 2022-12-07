from flask import current_app as app, flash
from flask_login import current_user


class Gift:
    def __init__(self, code, amount):
        self.code = code
        self.amount = amount

    def createCode(amount):
        rows = app.db.execute("""
INSERT INTO Gifts(code, amount)
VALUES(:code, :amount)
RETURNING code
""",
                                  code = code,
                                   amount = amount)
        return 1
    
    def get(code):
        print("gettig code")
        try:
            rows = app.db.execute("""
            SELECT code, amount
            FROM Gifts
            WHERE code = :code
    """,
                                    code = code)
            return Gift(*(rows[0])) if rows is not None else None
        except Exception as e:
            print(str(e))
            return None

    def removeCode(code):
        rows = app.db.execute("""
        DELETE 
        FROM Gifts 
        WHERE code = :code
""",
                                code = code)
        return 1