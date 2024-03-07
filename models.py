from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, select, join

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    company = db.Column(db.String(50), default='company name')
    house = db.Column(db.String(50), default='123')
    street = db.Column(db.String(50), default='street name')
    apartment = db.Column(db.String(50), default='blk 0')
    city = db.Column(db.String(50), default='Ontario')
    zipCode = db.Column(db.String(20), default='123456')
    country = db.Column(db.String(50), default='Canada')
    vatNumber = db.Column(db.String(50), default='123456')
