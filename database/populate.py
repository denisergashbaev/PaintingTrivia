from models.user import User
from settings import db
from models.painter import Painter
from models.painting import Painting
from models.saint import Saint


db.create_all()

painters = {
    'painter1': Painter('Van Gogh1'),
    'painter2': Painter('Van Gogh2'),
    'painter3': Painter('Van Gogh3'),
    'painter4': Painter('Van Gogh4')
}

paintings = {
    'painting1': Painting(painters['painter1'], 'Starry Night1',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting2': Painting(painters['painter2'], 'Starry Night2',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting3': Painting(painters['painter3'], 'Starry Night3',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting4': Painting(painters['painter4'], 'Starry Night4',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting5': Painting(painters['painter4'], 'Starry Night5',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting6': Painting(painters['painter4'], 'Starry Night5',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg')
}

saints = {
    'saint1': Saint('Saint George'),
    'saint2': Saint('Saint Stan'),
    'saint3': Saint('Saint Anthony'),
}



relationship_saints_painting = [
    [saints['saint1'], paintings['painting1']],
]

for painter in painters.values():
    db.session.add(painter)

for painting in paintings.values():
    db.session.add(painting)

for saint in saints.values():
    db.session.add(saint)

for saint,painting in relationship_saints_painting:
    print saint, painting
    saint.paintings.append(painting)

User.add_user('test', 'test')

db.session.commit()
