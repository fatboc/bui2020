from flask import flash, redirect, request, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Uzytkownik, Student, Prowadzacy
from ..tracer import tracer

@auth.route('/register', methods=['GET', 'POST'])
def register():
    with tracer.start_span('rejestracja') as span:
        span.set_tag('span.kind', 'server')
        span.set_tag('module', 'auth')
        span.set_tag('action', 'register')
        span.set_tag('tier', 'frontend')
        form = RegistrationForm()
        span.log_kv({'event':'init', 'object':'Form'})
        v = form.validate_on_submit()
        span.log_kv({'event':'validate', 'value' : v})

        if v:
            with tracer.start_active_span('db_add', child_of=span):
                span.set_tag('tier', 'backend')
                uzytkownik = Uzytkownik(nazwa=form.nazwa.data,
                                    password=form.haslo.data)
                span.log_kv({'event': 'object.create', 'object': 'Uzytkownik', 'value': uzytkownik.nazwa})
                nowy_numer = Uzytkownik.query.count()+1
                span.log_kv({'event': 'id.generate', 'object': 'Uzytkownik', 'value': uzytkownik.nazwa, 'value': nowy_numer})
                rodzaj = form.rodzaj.data
                span.log_kv({'event': 'form.read', 'object':'Uzytkownik', 'value': uzytkownik.nazwa, 'value': rodzaj})
        
                db.session.add(uzytkownik)
                span.log_kv({'event': 'db.add', 'object': 'Uzytkownik', 'value': uzytkownik.nazwa})
                db.session.commit()
                span.log_kv({'event': 'db.commit', 'object': 'Uzytkownik', 'value': uzytkownik.nazwa})
        
                if rodzaj=='Student':
                    student = Student.query.filter_by(nr_indeksu=form.nr_dokumentu.data)
                    span.log_kv({'event': 'db.query', 'object': 'Student', 'value': student.nr_indeksu})
                    student.update(dict(nr_uzytkownika=nowy_numer))
                    span.log_kv({'event': 'db.update', 'object': 'Student', 'value': student.nr_indeksu, 'value': nowy_numer})
        
                db.session.commit()
                span.log_kv({'event': 'db.commit', 'object': 'Student', 'value': student.nr_indeksu})
    
            
            flash('Rejestracja przebiegła pomyślnie.')
            span.log_kv({'event': 'user.print'})
    
            span.log_kv({'event': 'redirect', 'route': 'auth.login'})
            return redirect(url_for('auth.login'))
    
        span.log_kv({'event': 'form.render', 'route': 'auth.register'})
        return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    with tracer.start_span('login') as span:
        span.set_tag('span.kind', 'server')
        span.set_tag('module', 'auth')
        span.set_tag('action', 'login')
        span.set_tag('tier', 'frontend')
        form = LoginForm()
        span.log_kv({'event': 'init', 'object':'Form'})
        if form.validate_on_submit():
            with tracer.start_active_span('db_check', child_of=span):
                span.set_tag('tier', 'backend')
                uzytkownik = Uzytkownik.query.filter_by(nazwa=form.nazwa.data).first()
                span.log_kv({'event': 'init', 'object':'Form'})
                if uzytkownik is not None and uzytkownik.verify_password(
                        form.haslo.data):
                    # log employee in
                    login_user(uzytkownik)

                    # redirect to the dashboard page after login
                    return redirect(url_for('home.dashboard'))

                # when login details are incorrect
                else:
                    flash('Błędna nazwa użytkownika lub hasło.')

        # load login template
        return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    with tracer.start_span('logout') as span:
        logout_user()
        flash('Wylogowano.')

        # redirect to the login page
        return redirect(url_for('auth.login'))
