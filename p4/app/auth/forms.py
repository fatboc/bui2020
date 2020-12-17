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

    def validate_username(self, field):
        if Uzytkownik.query.filter_by(nazwa=field.data).first():
            raise ValidationError('Podana nazwa jest już zajęta.')

class IDFormStudent(FlaskForm):
    nr_indeksu = StringField('Numer Indeksu', validators=[DataRequired()])

    def validate_id(self, field):
        if UzytkownikStudent.query.filter_by(nr_indeksu=field.data).first():
            raise ValidationError('Podany indeks jest już zarejestrowany.')
        elif Student.query.filter_by(nr_indeksu=field.data) == None:
            raise ValidationError('Podany indeks nie istnieje')

class IDFormProwadzacy(FlaskForm):
    nr_prowadzacego = StringField('Numer Dokumentu', validators=[DataRequired()])

    def validate_id(self, field):
        if UzytkownikProwadzacy.query.filter_by(nr_prowadzacego=field.data).first():
            raise ValidationError('Podany numer jest już zarejestrowany.')
        elif Prowadzacy.query.filter_by(nr_prowadzacego=field.data) == None:
            raise ValidationError('Podany numer nie istnieje')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')
