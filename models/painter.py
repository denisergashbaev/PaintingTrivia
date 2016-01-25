from settings import db
from sqlalchemy.orm import relationship, backref
from models.artistic_movement import ArtisticMovement

artistic_movements = db.Table('painters_to_artistic_movements',
    db.Column('painter_id', db.Integer, db.ForeignKey('painter.id')),
    db.Column('artistic_movement_id', db.Integer, db.ForeignKey('artistic_movement.id'))
                              )


class Painter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    artistic_movements = relationship(ArtisticMovement, secondary=artistic_movements,
                             backref=db.backref('painters', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Painter %r>' % self.name