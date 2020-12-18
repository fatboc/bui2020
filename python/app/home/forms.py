# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class ZadanieForm(FlaskForm):
    nr_kursu = IntegerField('Numer kursu', validators=[DataRequired()])
    typ = StringField('Rodzaj zadania', validators=[DataRequired()])
    termin = DateField('Termin (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    opis = StringField('Opis zadania')
    submit = SubmitField('Zatwierdź')
    
