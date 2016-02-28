from settings import db, salt
import crypt
from sqlalchemy.sql.expression import and_


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def add_user(user_name, user_password):
        q = db.session.query(User).filter(User.name == user_name).all()

        # check if the user exist
        if not q:
            # Add user
            user = User(user_name, crypt.crypt(user_password, salt))
            db.session.add(user)
            db.session.commit()
            return user
        return None

    @staticmethod
    def get_user(user_name, user_password):
        retrieved_user = User.query.filter(and_(User.name == user_name,
                                                User.password == crypt.crypt(user_password, salt))).first()
        return retrieved_user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter(User.id == user_id).first()
