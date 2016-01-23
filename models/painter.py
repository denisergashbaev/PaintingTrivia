from settings import db
from sqlalchemy.orm import relationship, backref


artistic_movements = db.Table('artistic_movement',
    db.Column('painter_id', db.Integer, db.ForeignKey('painter.id')),
    db.Column('artisticmovement_id', db.Integer, db.ForeignKey('artisticmovement.id'))
)


class Painter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    artistic_movements = relationship('ArtisticMovement', secondary=artistic_movements,
                             backref=db.backref('painters', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Painter %r>' % self.name