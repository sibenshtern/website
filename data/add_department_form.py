from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    chief = IntegerField(validators=[DataRequired()])
    members = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    submit = SubmitField()
