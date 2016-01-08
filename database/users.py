from settings import db
from models.user import User
import crypt


def add_user(user_name, user_password):
    q = db.session.query(User).filter(User.name == user_name).all()

    # check if the user exist
    if not q:
        # Add user
        user = User(user_name, crypt.crypt(user_password, user_name))
        db.session.add(user)
        db.session.commit()
        return True
    return False


def check_user_password(user_name, user_password):
    retrieved_users = User.query.filter(User.name == user_name).all()
    if retrieved_users:
        return retrieved_users[0].password == crypt.crypt(user_password, user_name)
