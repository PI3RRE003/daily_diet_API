from database import db
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name_meal = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.String(80), nullable=False)
    diet_or_not = db.Column(db.String(80), nullable=False)