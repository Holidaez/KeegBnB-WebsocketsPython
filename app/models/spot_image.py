from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class SpotImage(db.Model):
    __tablename__ = 'spot_images'

    if environment == "production":
        __table_args__ = {'schema':SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(10001), nullable=False)
    preview_image = db.Column(db.Boolean)

    #? Foreign Keys
    spot_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('spots.id')), nullable=False)

    #! Many Side Relationships
    spot = db.relationship('Spot', back_populates='spot_images')

    #!One Side Relationships

    def to_dict(self):
        return {
            'id':self.id,
            'url':self.url,
            'spot_id':self.spot_id
        }
