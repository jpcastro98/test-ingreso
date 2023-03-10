from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

#Se crea el modelo usuario 
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    #se crea funcion en el modelo para registrar usuario 
    def user():
        email = "admin@admin.com"
        name =  "admin"
        password = "admin"
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

#Se crea el modelo Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    quality = db.Column(db.String(100))

