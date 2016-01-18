from settings import db


class Painting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    file_name = db.Column(db.String(255), unique=True)
    painter_id = db.Column(db.Integer, db.ForeignKey('painter.id'))
    painter = db.relationship("Painter")

    def __init__(self, painter, title, file_name):
        self.painter = painter
        self.title = title
        self.file_name = file_name

    def __repr__(self):
        return '<Painting %r>' % self.title