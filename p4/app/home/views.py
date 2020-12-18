# app/home/views.py

from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from . import home
from ..models import *
from ..tracer import tracer
from .. import db
from .forms import ZadanieForm


@home.route('/')
def homepage():
    with tracer.start_span('homepage') as span:
        return render_template('home/index.html', title="Bezpieczne Usługi internetowe")


@home.route('/dashboard')
@login_required
def dashboard():
    with tracer.start_span('dashboard') as span:
        student = Student.query.filter_by(nr_uzytkownika = current_user.id).first()
        return render_template('home/dashboard.html', title="Widok główny")

@home.route('/studenci')
@login_required
def pokaz_studentow():
    with tracer.start_span('studenci') as span:
        studenci = Student.query.all()

        return render_template('home/studenci/studenci.html', studenci=studenci, title="Studenci")

@home.route('/prowadzacy')
@login_required
def pokaz_prowadzacych():
    with tracer.start_span('prowadzacy') as span:
        prowadzacy = Prowadzacy.query.all()

        return render_template('home/prowadzacy/prowadzacy.html', prowadzacy=prowadzacy, title="Prowadzacy")

@home.route('/kursy')
@login_required
def pokaz_kursy():
    with tracer.start_span('kursy') as span:
        kursy = Kurs.query.all()
    
        return render_template('home/kursy/kursy.html', kursy=kursy, title="Kursy")

@home.route('/linki')
@login_required
def pokaz_linki():
    with tracer.start_span('linki') as span:
        linki = Link.query.all()
    
        return render_template('home/linki/linki.html', linki=linki, title="Linki")

@home.route('/zadania', methods=['GET', 'POST'])
@login_required
def pokaz_zadania():
    with tracer.start_span('pokaz_zadania') as span:
        zadania = Zadanie.query.filter_by(nr_uzytkownika=current_user.id)
    
        return render_template('home/zadania/zadania.html',
                           zadania=zadania, title="Zadania")


@home.route('/zadania/add', methods=['GET', 'POST'])
@login_required
def dodaj_zadanie():
    with tracer.start_span('dodaj_zadanie') as span:
        dodaj_zadanie = True

        form = ZadanieForm()
        if form.validate_on_submit():
            zadanie = Zadanie(nr_kursu=form.nr_kursu.data,
                              termin=form.termin.data,
                              typ=form.typ.data,
                              opis=form.opis.data,
                              nr_uzytkownika=current_user.id)

            with tracer.start_active_span('db_add', child_of=span):
                try:
                    db.session.add(zadanie)
                    db.session.commit()
                    flash('Zadanie dodane pomyślnie.')
                except:
                    flash('Coś nie pykło :(')

                return redirect(url_for('home.pokaz_zadania'))

        return render_template('home/zadania/zadanie.html', action="Add",
                           dodaj_zadanie=dodaj_zadanie, form=form,
                           title="Dodaj zadanie")


@home.route('/zadania/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edytuj_zadanie(id):
    with tracer.start_span('edytuj_zadanie') as span:

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
    with tracer.start_span('usun_zadanie') as span:
        zadanie = Zadanie.query.get_or_404(id)
        with tracer.start_active_span('db_delete', child_of=span):
            db.session.delete(zadanie)
            db.session.commit()
            flash('Zadanie usunięte pomślnie')

        # redirect to the departments page
        return redirect(url_for('home.pokaz_zadania'))

        return render_template(title="Usuń zadanie")
