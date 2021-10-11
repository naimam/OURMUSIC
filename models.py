from app import db


class Person(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    artists = db.relationship("Artist", backref="username", lazy="dynamic")

    def __repr__(self):
        return "<Username: {}>".format(self.username)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(22))

    def __repr__(self):
        return "<Artist Id: {}>".format(self.artist_id)
