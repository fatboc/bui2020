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

    nr_indeksu = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(16))
    nazwisko = db.Column(db.String(16))
    nr_uzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.nr_uzytkownika'), unique=True)

    def __repr__(self):
        return '<Student: {}>'.format(self.imie . self.nazwisko)

class Prowadzacy(db.Model):

    __tablename__ = 'prowadzacy'

    nr_prowadzacego = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(16))
    nazwisko = db.Column(db.String(16))
    nr_uzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.nr_uzytkownika'), unique=True)

    def __repr__(self):
        return '<Prowadzacy: {}>'.format(self.imie + self.nazwisko)

class Kurs(db.Model):

    __tablename__ = 'kursy_prowadzacy'

    nr_kursu = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255))
    prowadzacy = db.Column(db.String(33))

    def __repr__(self):
        return '<Kurs: {}>'.format(self.nazwa)

class Link(db.Model):
    __tablename__ = 'nowe_linki'

    nr_linku = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    nazwa = db.Column(db.String(255))
    linkk = db.Column(db.String(255))

    def __repr__(self):
        return '<Link: {}>'.format(self.linkk)

class UzytkownikStudent(db.Model):
    __tablename__ = 'uzytkownicy_studenci'

    nr_uzytkownika = db.Column(db.Integer, primary_key=True)
    nr_indeksu = db.Column(db.Integer)

    def __repr__(self):
        return '<Numerki: {}>'.format(self.nr_uzytkownika + self.nr_indeksu)

class UzytkownikProwadzacy(db.Model):
    __tablename__ = 'uzytkownicy_prowadzacy'

    nr_uzytkownika = db.Column(db.Integer, primary_key=True)
    nr_prowadzacego = db.Column(db.Integer)

    def __repr__(self):
        return '<Numerki: {}>'.format(self.nr_uzytkownika + self.nr_prowadzacego)

