from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Spot(db.Model):
    __tablename__ = "spots"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(501), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    #? Foreign Keys
    owner_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)

    #! Many Side relationships
    owner = db.relationship('User', back_populates='spots')
    reviews = db.relationship('Review', back_populates='spot')
    #! One Side Relationships
    spot_images = db.relationship('SpotImage', back_populates='spot')
    Review = db.relationship('Review', back_populates='spot')

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'lat':self.lat,
            'lng':self.lng,
            'state':self.state,
            'country':self.country,
            'city':self.city,
            'address': self.address,
            'description':self.description,
            'price':self.price
        }
