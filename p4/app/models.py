# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Uzytkownik(UserMixin, db.Model):

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'uzytkownicy'

    nr_uzytkownika = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(16), index=True, unique=True)
    haslo = db.Column(db.String(128))
    nr_studenta = db.Column(db.Integer, db.ForeignKey('studenci.nr_indeksu'))
    nr_prowadzacego = db.Column(db.Integer, db.ForeignKey('prowadzacy.nr_prowadzacego'))
    czy_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Uzytkownik: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Uzytkownik.query.get(int(nr_uzytkownika))


class Student(db.Model):

    __tablename__ = 'studenci'

    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(60), unique=True)
    nazwisko = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Student: {}>'.format(self.name)

