from settings import db
from sqlalchemy.orm import relationship

saint_to_painting = db.Table('saint_to_painting',
                             db.Column('saint_id', db.Integer, db.ForeignKey('saint.id')),
                             db.Column('painting_id', db.Integer, db.ForeignKey('painting.id'))
)


class Saint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    paintings = relationship('Painting', secondary=saint_to_painting,
                                     backref=db.backref('saints', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Saint %r>' % self.name
