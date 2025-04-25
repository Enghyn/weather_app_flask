from database import db

class Ciudad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40))
    pais = db.Column(db.String(40))
    temperatura = db.Column(db.Integer)
    presion = db.Column(db.Integer)
    humedad = db.Column(db.Integer)