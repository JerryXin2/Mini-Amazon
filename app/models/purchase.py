from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT seller_id, uid, product_id, order_time
FROM Orders
WHERE uid = :uid
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT seller_id, uid, product_id, order_time
FROM Orders
WHERE uid = :uid
AND order_time >= :since
ORDER BY order_time DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
