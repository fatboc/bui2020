# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
#from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Uzytkownik


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        uzytkownik = uzytkownik(nazwa=form.nazwa.data,
                            haslo=form.haslo.data)

        rodzaj = form.rodzaj.data
        if rodzaj=='Student':
            dokument = IDFormStudent()
            if form.validate_on_submit():
                db.session.add(uzytkownik)
                student = Student.query.filter_by(nr_indeksu=dokument.nr_indeksu.data).update(dict(nr_uzytkownika=uzytkownik.nr_uzytkownika))

        elif rodzaj=='Prowadzacy':
            dokument = IDFormProwadzacy()
            if form.validate_on_submit():
                db.session.add(uzytkownik)
                prowadzacy = prowadzacy.query.filter_by(nr_prowadzacego=dokument.nr_indeksu.data).update(dict(nr_uzytkownika=uzytkownik.nr_uzytkownika))


        # add employee to the database
        db.session.commit()
        flash('Rejestracja przebiegła pomyślnie.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
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
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('Wylogowano.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
