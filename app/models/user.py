from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .direct_messages import DirectMessage


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    #! One Side Relationships
    spots = db.relationship('Spot', back_populates='owner')
    reviews = db.relationship('Review', back_populates='user')

    #! Many Side Relationships
    sender = db.relationship(
        "User",
        secondary="direct_messages",
        primaryjoin=(id == DirectMessage.sender_id),
        secondaryjoin=(id == DirectMessage.recipient_id),
    )
    direct_messages2 = db.relationship(
        "User",
        secondary="direct_messages",
        primaryjoin=(id == DirectMessage.recipient_id),
        secondaryjoin=(id == DirectMessage.sender_id),
        overlaps="sender"
    )
    likes = db.relationship('Like', back_populates='user')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
