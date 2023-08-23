from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Like(db.Model):
    __tablename__ = 'likes'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}


    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')))
    review_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('reviews.id')))

    user = db.relationship('User', back_populates='likes')
    review = db.relationship("Review", back_populates='likes')

    def to_dict(self):
        return {
            'id':self.id,
            'user':self.user.id
        }
