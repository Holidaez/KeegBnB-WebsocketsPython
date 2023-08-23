from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Review(db.Model):
    __tablename__ = 'reviews'

    if environment == "production":
        __table_args__ = {'schema':SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)

    #? Foreign Keys
    spot_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('spots.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)

    #! Many Side relationships
    user = db.relationship('User', back_populates='reviews')
    spot = db.relationship('Spot', back_populates='reviews')

    #! One Side Relationships
    review_images = db.relationship('ReviewImage', back_populates='review')
    likes = db.relationship('Like', back_populates='review')

    def to_dict(self):
        return {
            'id':self.id,
            'review':self.review,
            'stars':self.stars,
            'spot_id':self.spot_id,
            'user_id':self.user_id
        }
