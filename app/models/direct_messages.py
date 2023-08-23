from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class DirectMessage(db.Model):
    __tablename__ = "direct_messages"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(5000), nullable=False)
    sent_at = db.Column(db.String(100), nullable=False)
    #? Foreign Keys
    sender_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')))
    recipient_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')))
    #! One Side Relationship

    #! Many Side Relationship
    # sender = db.relationship('User', back_populates='sender')
    # recipient = db.relationship('User',back_populates='recipient')

    def to_dict(self):
        return {
            'id':self.id,
            'msg':self.message,
            'sender_id':self.sender_id,
            'recipient_id':self.recipient_id
        }
