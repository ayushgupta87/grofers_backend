from db import db


class DatabaseModel(db.Model):
    __tablename__ = 'items_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price_per_kg = db.Column(db.String(5), nullable=False)
    discount_percentage = db.Column(db.String(3), nullable=False)
    item_category = db.Column(db.String(20), nullable=False)
    item_image = db.Column(db.Text, default='NONE')

    def __init__(self, name, price_per_kg, discount_percentage, item_category, item_image):
        self.name = name
        self.price_per_kg = price_per_kg
        self.discount_percentage = discount_percentage
        self.item_category = item_category
        self.item_image = item_image

    def item_json(self):
        return {
            'name': self.name,
            'perKgpPrice': self.price_per_kg,
            'discount': self.discount_percentage,
            'category' : self.item_category,
            'image': self.item_image
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_by_category(cls, item_category):
        return cls.query.filter_by(item_category=item_category).query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



