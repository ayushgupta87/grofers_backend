from db import db


class UserModel(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def user_json(self):
        return {
            'name': self.name,
            'username': self.username
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
