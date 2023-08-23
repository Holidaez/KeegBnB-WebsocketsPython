from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import DirectMessage



def check_len(form,field):
    print("OPEN BLOCK ------------------------>")
    print(form)
    print(form.data)
    print(field)
    print(field.data)
    print("Close BLOCK ------------------------>")

class DirectMessageForm(FlaskForm):
    message = StringField('message', validators=[DataRequired(), check_len])
