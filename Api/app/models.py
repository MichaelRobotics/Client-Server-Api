from .extensions import db

class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
