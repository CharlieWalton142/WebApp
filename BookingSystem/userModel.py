from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime



class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    admin = db.Column(db.Integer)
    notes = db.relationship('Note')
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Booking(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    training_type = db.Column(db.String(50), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    
