from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User, Spot


class SpotForm(FlaskForm):
    owner_id = IntegerField('owner')
    name = StringField('name',validators=[DataRequired(), Length(min=3,max=25, message='Name must be between 3 and 25 characters')])
    lat = IntegerField('lat',validators=[DataRequired()])
    lng = IntegerField('lng',validators=[DataRequired()])
    state = StringField('state',validators=[DataRequired(), Length(min=2,max=15, message='State must be between 2 and 15 characters')])
    country = StringField('country',validators=[DataRequired(), Length(min=3,max=50, message='Country must be between 3 and 50 characters')])
    city = StringField('city',validators=[DataRequired(), Length(min=3,max=50, message='City must be between 3 and 50 characters')])
    address = StringField('address',validators=[DataRequired(), Length(min=3,max=150, message='Address must be between 3 and 150 characters')])
    description = StringField('description',validators=[DataRequired(), Length(min=3,max=500, message='Description must be between 3 and 500 characters')])
    price = IntegerField('price', validators=[DataRequired()])
