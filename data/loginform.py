from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField(
        'Пароль астронавта', validators=[DataRequired()])
    captain_id = StringField('ID капитана', validators=[DataRequired()])
    captain_password = PasswordField(
        'Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')

