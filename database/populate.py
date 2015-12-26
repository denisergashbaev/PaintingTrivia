# coding=utf-8
from settings import db
from models.painter import Painter
from models.painting import Painting

#creates tables (schema)
db.create_all()

painters = {
    'painter1': Painter(u'Vincent van Gogh'),
    'painter2': Painter(u'Pierre-Auguste Renoir'),
    'painter3': Painter(u'Édouard Manet'),
    'painter4': Painter(u'Claude Monet')
}

paintings = [
    Painting(painters['painter1'], u'Starry Night', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter2'], u'Bal du moulin de la Galette', 'Bal_moulin_Galette_renoir.jpg'),
    Painting(painters['painter3'], u'Chez le père Lathuille', 'at-father-lathuille.jpg'),
    Painting(painters['painter4'], u'Le Déjeuner sur l’herbe', 'Monet_dejeunersurlherbe.jpg'),
]

for painter in painters.values():
    db.session.add(painter)

for painting in paintings:
    db.session.add(painting)

db.session.commit()