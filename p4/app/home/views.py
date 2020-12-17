# app/home/views.py

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import home
from ..models import *
from .. import db


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


