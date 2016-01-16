# coding=utf-8
from settings import db
from models.user import User
from models.painter import Painter
from models.painting import Painting

db.create_all()

painters = {
    'painter1': Painter(u'Vincent van Gogh'),
    'painter2': Painter(u'Pierre-Auguste Renoir'),
    'painter3': Painter(u'Édouard Manet'),
    'painter4': Painter(u'Claude Monet'),
    'painter5': Painter(u'Alfred Sisley'),
    'painter6': Painter(u'Camille Pissarro'),
    'painter7': Painter(u'Mary Cassatt'),
    'painter8': Painter(u'Berthe Morisot'),
    'painter9': Painter(u'Armand Guillaumin'),
    'painter10': Painter(u'Gustave Caillebotte'),
    'painter11': Painter(u'Georges Seurat'),

    'painter12': Painter(u'Francisco de Zurbarán'),
    'painter13': Painter(u'Michelangelo Merisi da Caravaggio'),
    'painter14': Painter(u'Emmanuel Tzanes'),
    'painter15': Painter(u'El greco'),

}


paintings = [
    Painting(painters['painter1'], u'Starry Night', '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    Painting(painters['painter2'], u'Bal du moulin de la Galette', 'Bal_moulin_Galette_renoir.jpg'),
    Painting(painters['painter2'], u'Le déjeuner des canotiers', 'renoir_dejeurner_canotier.jpg'),
    Painting(painters['painter3'], u'Chez le père Lathuille', 'at-father-lathuille.jpg'),
    Painting(painters['painter4'], u'Le Déjeuner sur l’herbe', 'Monet_dejeunersurlherbe.jpg'),
    Painting(painters['painter4'], u'The Cliffs at Etretat', 'Claude_Monet_The_Cliffs_at_Etretat.jpg'),

    Painting(painters['painter12'], u'Santa Lucía de Siracusa', 'zurbaran_lucia.jpg'),
    Painting(painters['painter13'], u'San Jeroni Escribiendo', 'caravaggio_san_gerolamo.jpg'),
    Painting(painters['painter13'], u'Saint Denis\' Marthyr', 'martirio_s_denis.jpg'),
    Painting(painters['painter14'], u'Saint Mark', 'Emmanuel_Tzane_Mark.jpg'),
    Painting(painters['painter15'], u'Saint Luke', 'san_lucas_greco.jpg'),
    Painting(painters['painter13'], u'Inspiració de sant Mateo', 'inspiracion_de_san_mateo_caravaggio.jpg'),
    Painting(painters['painter15'], u'Sant Joan Evangelista', 'san_Juan_Evangelista_el_greco.jpg'),
]


for painter in painters.values():
    db.session.add(painter)

for painting in paintings:
    db.session.add(painting)

User.add_user('test', 'test')

db.session.commit()