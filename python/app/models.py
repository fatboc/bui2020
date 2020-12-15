from app import db

class Studenci(db.Model):
    __tablename__ = 'studenci'

    nr_indeksu = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(16), index=True)
    nazwisko = db.Column(db.String(16), index=True)


class Prowadzacy(db.Model):
    __tablename__ = 'prowadzacy'

    nr_prowadzacego = db.Column(db.Integer, unique = True, primary_key=True)
    imie = db.Column(db.String(16), index=True)
    nazwisko = db.Column(db.String(16), index=True)

class Kursy(db.Model):
    __tablename__ = 'kursy'

    nr_kursu = db.Column(db.Integer, unique = True, primary_key = True)
    nazwa = db.Column(db.String(255)) 
    nr_gl_prowadzacego = db.Column(db.Integer, db.ForeignKey('prowadzacy.nr_prowadzacego'))

