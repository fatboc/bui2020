# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from ..models import Student


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    haslo = PasswordField('Hasło', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    potwierdz_haslo = PasswordField('Potwierdź hasło')
    rodzaj = RadioField('Rodzaj użytkownika', choices=['Student', 'Prowadzacy'], validators=[DataRequired()])
    nr_dokumentu = StringField('Numer Dokumentu', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

    def validate_id(self, field):
        if Student.query.filter_by(nr_indeksu=field.data).first():
            raise ValidationError('ID is already in use.')

    def validate_username(self, field):
        if Uzytkownik.query.filter_by(nazwa=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')
