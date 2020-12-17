# app/home/views.py

from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from . import home
from ..models import *
from .. import db
from .forms import ZadanieForm


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Bezpieczne Usługi internetowe")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    student = Student.query.filter_by(nr_uzytkownika = current_user.id).first()
    kursy_studenta = KursyStudenta.query.filter_by(nr_indeksu=student.nr_indeksu)
    return render_template('home/dashboard.html', title="Widok główny")

@home.route('/studenci')
@login_required
def pokaz_studentow():
    studenci = Student.query.all()

    return render_template('home/studenci/studenci.html', studenci=studenci, title="Studenci")

@home.route('/prowadzacy')
@login_required
def pokaz_prowadzacych():
    prowadzacy = Prowadzacy.query.all()

    return render_template('home/prowadzacy/prowadzacy.html', prowadzacy=prowadzacy, title="Prowadzacy")

@home.route('/kursy')
@login_required
def pokaz_kursy():
    kursy = Kurs.query.all()

    return render_template('home/kursy/kursy.html', kursy=kursy, title="Kursy")

@home.route('/linki')
@login_required
def pokaz_linki():
    linki = Link.query.all()

    return render_template('home/linki/linki.html', linki=linki, title="Linki")

@home.route('/zadania', methods=['GET', 'POST'])
@login_required
def pokaz_zadania():

    zadania = Zadanie.query.filter_by(nr_uzytkownika=current_user.id)

    return render_template('home/zadania/zadania.html',
                           zadania=zadania, title="Zadania")


@home.route('/zadania/add', methods=['GET', 'POST'])
@login_required
def dodaj_zadanie():

    dodaj_zadanie = True

    form = ZadanieForm()
    if form.validate_on_submit():
        zadanie = Zadanie(nr_kursu=form.nr_kursu.data,
                          termin=form.termin.data,
                          typ=form.typ.data,
                          opis=form.opis.data,
                          nr_uzytkownika=current_user.id)

        #try:
        db.session.add(zadanie)
        db.session.commit()
        flash('Zadanie dodane pomyślnie.')
        #except:
        flash('Coś nie pykło :(')

        return redirect(url_for('home.pokaz_zadania'))

    return render_template('home/zadania/zadanie.html', action="Add",
                           dodaj_zadanie=dodaj_zadanie, form=form,
                           title="Dodaj zadanie")


@home.route('/zadania/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edytuj_zadanie(id):

    dodaj_zadanie = False

    zadanie = Zadanie.query.get_or_404(id)
    form = ZadanieForm(obj=zadanie)
    if form.validate_on_submit():
        nr_kursu=form.nr_kursu.data,
        termin=form.termin.data,
        typ=form.typ.data,
        opis=form.opis.data,
        db.session.commit()
        flash('Zadanie edytowane pomyślnie')

        # redirect to the departments page
        return redirect(url_for('home.pokaz_zadania'))

    form.nr_kursu.data=nr_kursu
    form.termin.data=termin
    form.typ.data=typ
    form.opis.data=opis
    return render_template('home/zadania/zadanie.html', action="Edit",
                           dodaj_zadanie=dodaj_zadanie, form=form,
                           zadanie=zadanie, title="Edytuj zadanie")


@home.route('/zadania/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def usun_zadanie(id):

    zadanie = Zadanie.query.get_or_404(id)
    db.session.delete(zadanie)
    db.session.commit()
    flash('Zadanie usunięte pomślnie')

    # redirect to the departments page
    return redirect(url_for('home.pokaz_zadania'))

    return render_template(title="Usuń zadanie")
