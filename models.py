from typing import DefaultDict
from flask_login import UserMixin
from __init__ import db
from datetime import datetime
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Expense(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.String(30))
    desc = db.Column(db.String(500))
    expense = db.Column(db.Integer)
    datetime=db.Column(db.String(500))

class dummy_table(UserMixin, db.Model):
    Transaction_Id = db.Column(db.Integer, primary_key=True) 
    Account_No= db.Column(db.String(30))
    Category = db.Column(db.String(30))
    Expense = db.Column(db.Integer)
    Date = db.Column(db.String(500))
    Purpose = db.Column(db.String(500))