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
        span.set_tag('module', 'home')
        return render_template('home/index.html', title="Bezpieczne Usługi internetowe")


@home.route('/dashboard')
@login_required
def dashboard():
    with tracer.start_span('dashboard') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)
        span.log_kv({'event': 'db.query', 'object': 'Student'})
        return render_template('home/dashboard.html', title="Widok główny")

@home.route('/studenci')
@login_required
def pokaz_studentow():
    with tracer.start_span('studenci') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)
        studenci = Student.query.all()
        span.log_kv({'event': 'db.query', 'object': 'Student'})

        return render_template('home/studenci/studenci.html', studenci=studenci, title="Studenci")

@home.route('/prowadzacy')
@login_required
def pokaz_prowadzacych():
    with tracer.start_span('prowadzacy') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        prowadzacy = Prowadzacy.query.all()
        span.log_kv({'event': 'db.query', 'object': 'Prowadzacy'})

        return render_template('home/prowadzacy/prowadzacy.html', prowadzacy=prowadzacy, title="Prowadzacy")

@home.route('/kursy')
@login_required
def pokaz_kursy():
    with tracer.start_span('kursy') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        kursy = Kurs.query.all()
        span.log_kv({'event': 'db.query', 'object': 'Kursy'})
    
        return render_template('home/kursy/kursy.html', kursy=kursy, title="Kursy")

@home.route('/linki')
@login_required
def pokaz_linki():
    with tracer.start_span('linki') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        linki = Link.query.all()
        span.log_kv({'event': 'db.query', 'object': 'Linki'})
    
        return render_template('home/linki/linki.html', linki=linki, title="Linki")

@home.route('/zadania', methods=['GET', 'POST'])
@login_required
def pokaz_zadania():
    with tracer.start_span('pokaz_zadania') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        zadania = Zadanie.query.filter_by(nr_uzytkownika=current_user.id)
        span.log_kv({'event': 'db.query', 'object': 'Zadania'})
    
        return render_template('home/zadania/zadania.html',
                           zadania=zadania, title="Zadania")


@home.route('/zadania/add', methods=['GET', 'POST'])
@login_required
def dodaj_zadanie():
    with tracer.start_span('dodaj_zadanie') as span:
        dodaj_zadanie = True
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        form = ZadanieForm()
        span.log_kv({'event':'init', 'object':'Form'})
        v = form.validate_on_submit()
        span.log_kv({'event':'validate', 'value' : v})
        if v:
            zadanie = Zadanie(nr_kursu=form.nr_kursu.data,
                              termin=form.termin.data,
                              typ=form.typ.data,
                              opis=form.opis.data,
                              nr_uzytkownika=current_user.id)
            span.log_kv({'event': 'object.create', 'object': 'Zadanie'})

            with tracer.start_active_span('db_add', child_of=span):
                try:
                    db.session.add(zadanie)
                    span.log_kv({'event': 'db.add', 'object': 'Zadanie'})
                    db.session.commit()
                    span.log_kv({'event': 'db.commit', 'object': 'Zadanie'})
                    flash('Zadanie dodane pomyślnie.')
                    span.log_kv({'event': 'user.print'})
                except:
                    flash('Coś nie pykło :(')
                    span.log_kv({'event': 'user.print'})

                return redirect(url_for('home.pokaz_zadania'))

        return render_template('home/zadania/zadanie.html', action="Add",
                           dodaj_zadanie=dodaj_zadanie, form=form,
                           title="Dodaj zadanie")


@home.route('/zadania/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edytuj_zadanie(id):
    with tracer.start_span('edytuj_zadanie') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        dodaj_zadanie = False
    
        zadanie = Zadanie.query.get_or_404(id)
        span.log_kv({'event': 'db.query', 'object': 'Zadanie'})
        form = ZadanieForm(obj=zadanie)
        span.log_kv({'event':'init', 'object':'Form'})

        v = form.validate_on_submit()
        span.log_kv({'event':'validate', 'value' : v})
        if v:
            nr_kursu=form.nr_kursu.data,
            termin=form.termin.data,
            typ=form.typ.data,
            opis=form.opis.data,
            span.log_kv({'event': 'db.update', 'object': 'Zadanie'})
            db.session.commit()
            span.log_kv({'event': 'db.commit', 'object': 'Zadanie'})
            flash('Zadanie edytowane pomyślnie')
            span.log_kv({'event': 'user.print'})
    
            # redirect to the departments page
            return redirect(url_for('home.pokaz_zadania'))
    
        form.nr_kursu.data=zadanie.nr_kursu
        form.termin.data=zadanie.termin
        form.typ.data=zadanie.typ
        form.opis.data=zadanie.opis
        span.log_kv({'event': 'form.update', 'object': 'Zadanie'})
        return render_template('home/zadania/zadanie.html', action="Edit",
                               dodaj_zadanie=dodaj_zadanie, form=form,
                               zadanie=zadanie, title="Edytuj zadanie")


@home.route('/zadania/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def usun_zadanie(id):
    with tracer.start_span('usun_zadanie') as span:
        span.set_tag('module', 'home')
        span.set_tag('user', current_user.id)

        zadanie = Zadanie.query.get_or_404(id)
        span.log_kv({'event': 'db.query', 'object': 'Zadanie'})
        with tracer.start_active_span('db_delete', child_of=span):
            db.session.delete(zadanie)
            span.log_kv({'event': 'db.delete', 'object': 'Zadanie'})
            db.session.commit()
            span.log_kv({'event': 'db.commit', 'object': 'Zadanie'})
            flash('Zadanie usunięte pomślnie')
            span.log_kv({'event': 'user.print'})

        # redirect to the departments page
        return redirect(url_for('home.pokaz_zadania'))

        return render_template(title="Usuń zadanie")
