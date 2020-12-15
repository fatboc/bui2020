# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from ..models import Student


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    imie = StringField('Imie', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    nazwisko = StringField('nazwisko', validators=[DataRequired()])
    imie = PasswordField('imie', validators=[DataRequired()])
    submit = SubmitField('Login')
