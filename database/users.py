from settings import db
from models.user import User

# creates tables (schema)
db.create_all()


def add_user(user_name, user_password):

    q = db.session.query(User).filter(User.name == user_name).all()

    # check if the user exist
    if not q:
        # Add user
        print user_name, user_password
        user = User(user_name, user_password)
        db.session.add(user)
        db.session.commit()
        return True
    return False


def check_user_password(user_name, user_password):
    q = db.session.query(User).filter(User.name == user_name).all()
    if q:
        # Add user
        if q.password == user_password:
            return True
    return False
