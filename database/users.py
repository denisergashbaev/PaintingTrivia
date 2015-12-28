from settings import db
from models.user import User

# creates tables (schema)
db.create_all()


def add_user(user_name, user_password):
    # if does not exits, create it


    # check if the user exist
    # existing_user_name = User.query.filter(User.name == user_name)
    q = db.session.query(User).filter(User.name == user_name).all()
    # print 'HERE', existing_user_name.user.name, existing_user_name.user.password_
    if not q:
        # Add user
        print user_name, user_password
        user = User(user_name, user_password)
        db.session.add(user)
        db.session.commit()
        return True
    return False
