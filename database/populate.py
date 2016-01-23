# coding=utf-8
from models.user import User
from settings import db
from models.artistic_movement import ArtisticMovement
from models.painter import Painter
from models.painting import Painting
from models.saint import Saint


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

paintings = {
    'painting1': Painting(painters['painter1'], u'Starry Night',
                          '1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg'),
    'painting2': Painting(painters['painter2'], u'Bal du moulin de la Galette', 'Bal_moulin_Galette_renoir.jpg'),
    'painting3': Painting(painters['painter2'], u'Le déjeuner des canotiers', 'renoir_dejeurner_canotier.jpg'),
    'painting4': Painting(painters['painter3'], u'Chez le père Lathuille', 'at-father-lathuille.jpg'),
    'painting5': Painting(painters['painter4'], u'Le Déjeuner sur l’herbe', 'Monet_dejeunersurlherbe.jpg'),
    'painting6': Painting(painters['painter4'], u'The Cliffs at Etretat', 'Claude_Monet_The_Cliffs_at_Etretat.jpg'),

    'painting7': Painting(painters['painter12'], u'Santa Lucía de Siracusa', 'zurbaran_lucia.jpg'),
    'painting8': Painting(painters['painter13'], u'San Jeroni Escribiendo', 'caravaggio_san_gerolamo.jpg'),
    'painting9': Painting(painters['painter13'], u'Saint Denis\' Marthyr', 'martirio_s_denis.jpg'),
    'painting10': Painting(painters['painter14'], u'Saint Mark', 'Emmanuel_Tzane_Mark.jpg'),
    'painting11': Painting(painters['painter15'], u'Saint Luke', 'san_lucas_greco.jpg'),
    'painting12': Painting(painters['painter13'], u'Inspiració de sant Mateo',
                           'inspiracion_de_san_mateo_caravaggio.jpg'),
    'painting13': Painting(painters['painter15'], u'Sant Joan Evangelista', 'san_Juan_Evangelista_el_greco.jpg'),
}

saints = {
    'saint1': Saint('Saint Luke'),
    'saint2': Saint('Saint Mark'),
    'saint3': Saint('Saint Joan Evangelist'),
    'saint4': Saint('Saint Mateo'),
    'saint5': Saint('Saint Denis'),
    'saint6': Saint('Saint Jeroni'),
    'saint7': Saint('Saint Lucia'),
    'saint8': Saint('Saint Albert'),

}

artistic_movements = {
    'artistic_movement_1': ArtisticMovement('Impressionism'),
    'artistic_movement_2': ArtisticMovement('Post-Impressionism'),
    'artistic_movement_3': ArtisticMovement('Baroque'),
    'artistic_movement_4': ArtisticMovement('Romanticism'),
}

# Relationship saints to painting:
saints['saint1'].paintings.extend([paintings['painting11']])
saints['saint2'].paintings.extend([paintings['painting10']])
saints['saint3'].paintings.extend([paintings['painting13']])
saints['saint4'].paintings.extend([paintings['painting12']])
saints['saint5'].paintings.extend([paintings['painting9']])
saints['saint6'].paintings.extend([paintings['painting8']])
saints['saint7'].paintings.extend([paintings['painting7']])

# Relationship painter to artistic movement
painters['painter1'].artistic_movements.extend([artistic_movements['artistic_movement_2']])


for painter in painters.values():
    db.session.add(painter)

for painting in paintings.values():
    db.session.add(painting)

for saint in saints.values():
    db.session.add(saint)


User.add_user('test', 'test')

db.session.commit()
