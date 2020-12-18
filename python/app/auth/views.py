from flask import flash, redirect, request, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Uzytkownik, Student, Prowadzacy
from ..tracer import tracer

@auth.route('/register', methods=['GET', 'POST'])
def register():
    with tracer.start_span('rejestracja') as span:
        span.set_tag('module', 'auth')
        form = RegistrationForm()
        span.log_kv({'event':'init', 'object':'Form'})
        v = form.validate_on_submit()
        span.log_kv({'event':'validate', 'value' : v})

        if v:
            with tracer.start_active_span('db_add', child_of=span) as cspan:
                uzytkownik = Uzytkownik(nazwa=form.nazwa.data,
                                    password=form.haslo.data)
                span.log_kv({'event': 'object.create', 'object': 'Uzytkownik'})
                nowy_numer = Uzytkownik.query.count()+1
                span.log_kv({'event': 'id.generate', 'object': 'Uzytkownik', 'value': nowy_numer})
                rodzaj = form.rodzaj.data
                span.log_kv({'event': 'form.read', 'object':'Uzytkownik', 'value': rodzaj})
        
                db.session.add(uzytkownik)
                span.log_kv({'event': 'db.add', 'object': 'Uzytkownik'})
                db.session.commit()
                span.log_kv({'event': 'db.commit', 'object': 'Uzytkownik'})
        
                if rodzaj=='Student':
                    student = Student.query.filter_by(nr_indeksu=form.nr_dokumentu.data).update(dict(nr_uzytkownika=nowy_numer))
                    span.log_kv({'event': 'db.query', 'object': 'Student'})
                    span.log_kv({'event': 'db.update', 'object': 'Student', 'value': nowy_numer})
        
                db.session.commit()
                span.log_kv({'event': 'db.commit', 'object': 'Student'})
    
            
            flash('Rejestracja przebiegła pomyślnie.')
            span.log_kv({'event': 'user.print'})
    
            return redirect(url_for('auth.login'))
    
        return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    with tracer.start_span('login') as span:
        span.set_tag('module', 'auth')
        form = LoginForm()
        span.log_kv({'event': 'init', 'object':'Form'})
        v = form.validate_on_submit()
        span.log_kv({'event':'validate', 'value' : v})
        if v:
            with tracer.start_active_span('db_check', child_of=span):
                uzytkownik = Uzytkownik.query.filter_by(nazwa=form.nazwa.data).first()
                span.log_kv({'event': 'db.query', 'object':'Uzytkownik'})
                u = uzytkownik is not None and uzytkownik.verify_password
                span.log_kv({'event': 'session.authenticate', 'value': u})
                if u:
                    login_user(uzytkownik)
                    span.log_kv({'event': 'session.start', 'value': uzytkownik.nazwa})
                    return redirect(url_for('home.dashboard'))

                else:
                    flash('Błędna nazwa użytkownika lub hasło.')
                    span.log_kv({'event': 'user.print'})

        return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    with tracer.start_span('logout') as span:
        span.set_tag('module', 'auth')
        span.set_tag('user', current_user.id)
        nazwa = current_user.nazwa
        logout_user()
        span.log_kv({'event': 'session.end'})
        flash('Wylogowano.')
        span.log_kv({'event': 'user.print'})

        # redirect to the login page
        return redirect(url_for('auth.login'))
