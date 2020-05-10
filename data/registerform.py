from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            EqualTo('repeat_password', message="Password must match")
        ]
    )
    repeat_password = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Password must match")
        ]
    )
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Sign up')
