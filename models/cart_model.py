from db import db


class CartModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.String(5), nullable=False)
    kg = db.Column(db.String(5), nullable=False)
    price = db.Column(db.String(5), nullable=False)
    note = db.Column(db.String(20), default='NONE')
    checkout = db.Column(db.String(2), default='0')

    def __init__(self, username, item, qty, kg, price, note='NONE', checkout='0'):
        self.username = username
        self.item = item
        self.qty = qty
        self.kg = kg
        self.price = price
        self.note = note
        self.checkout = checkout

    def cart_json(self):
        return {
            'username': self.username,
            'item': self.item,
            'qty': self.qty,
            'kg': self.kg,
            'price': self.price,
            'note': self.note
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username_item_cart(cls, username, item):
        return cls.query.filter_by(username=username,
                                   item=item,
                                   checkout='0').first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()