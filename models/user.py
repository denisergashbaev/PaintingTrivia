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
            return True
        return False

    @staticmethod
    def check_user_password(user_name, user_password):
        retrieved_users = User.query.filter(and_(User.name == user_name, User.password == crypt.crypt(user_password, salt))
                                            ).first()
        return retrieved_users is not None
