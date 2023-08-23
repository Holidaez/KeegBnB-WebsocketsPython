from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class ReviewImage(db.Model):
    __tablename__ = 'review_images'

    if environment == "production":
        __table_args__ = {'schema':SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(10000), nullable=False)

    #? Foreign Keys
    review_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('reviews.id')), nullable=False)

    #! Many Side Relationships
    review = db.relationship('Review', back_populates='review_images')

    #!One Side Relationships

    def to_dict(self):
        return {
            'id':self.id,
            'url':self.url,
            'review_id':self.review_id
        }
