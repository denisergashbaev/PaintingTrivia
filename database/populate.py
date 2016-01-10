from models.user import User
from settings import db
from models.painter import Painter
from models.painting import Painting

#creates tables (schema)
db.create_all()

painters = {
    'painter1': Painter('Van Gogh1'),
    'painter2': Painter('Van Gogh2'),
    'painter3': Painter('Van Gogh3'),
    'painter4': Painter('Van Gogh4')
}

paintings = [
    Painting(painters['painter1'], 'Starry Night1', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter2'], 'Starry Night2', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter3'], 'Starry Night3', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter4'], 'Starry Night4', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter4'], 'Starry Night5', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter4'], 'Starry Night5', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg')
]

for painter in painters.values():
    db.session.add(painter)

for painting in paintings:
    db.session.add(painting)

User.add_user('test', 'test')

db.session.commit()