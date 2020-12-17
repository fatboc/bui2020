# app/auth/views.py

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
        form = RegistrationForm()
        if form.validate_on_submit():
            with tracer.start_active_span('db_add', child_of=span):
                uzytkownik = Uzytkownik(nazwa=form.nazwa.data,
                                    password=form.haslo.data)
                nowy_numer = Uzytkownik.query.count()+1
                rodzaj = form.rodzaj.data
        
                db.session.add(uzytkownik)
                db.session.commit()
        
                if rodzaj=='Student':
                    student = Student.query.filter_by(nr_indeksu=form.nr_dokumentu.data).update(dict(nr_uzytkownika=nowy_numer))
        
                db.session.commit()
    
            # add employee to the database
            flash('Rejestracja przebiegła pomyślnie.')
    
            # redirect to the login page
            return redirect(url_for('auth.login'))
    
        # load registration template
        return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    with tracer.start_span('login') as span:
        form = LoginForm()
        if form.validate_on_submit():
            with tracer.start_active_span('db_check', child_of=span):
                uzytkownik = Uzytkownik.query.filter_by(nazwa=form.nazwa.data).first()
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
