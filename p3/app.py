from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from jaeger_client import Config
from flask_opentracing import FlaskTracing
import logging
import time

def say_hello(hello_to):
    with tracer.start_span('say-hello') as span:
        hello_str = 'Hello, %s!' % hello_to
        print(hello_str)

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'jaeger-agent',
                'reporting_port': '6831',
            },
            'logging': True,
        },
        service_name='bui2020',
        validate=True,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()
tracer = init_tracer('hello-world')
app = Flask(__name__)


app.secret_key = 'Secret Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bui2020:BUI-zimowy-2020@sql/studia'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

say_hello('eluwa')

time.sleep(2)
tracer.close()

#Creating model table for our CRUD database
class Studenci(db.Model):
    __tablename__ = 'studenci'

    nr_indeksu = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(16), index=True)
    nazwisko = db.Column(db.String(16), index=True)
    
    def __init__(self, nr_indeksu, imie, nazwisko):
       self.nr_indeksu = nr_indeksu
       self.imie = imie
       self.nazwisko = nazwisko


class Prowadzacy(db.Model):
    __tablename__ = 'prowadzacy'

    nr_prowadzacego = db.Column(db.Integer, unique = True, primary_key=True)
    imie = db.Column(db.String(16), index=True)
    nazwisko = db.Column(db.String(16), index=True)
    
    def __init__(self, nr_prowadzacego, imie, nazwisko):
        self.nr_prowadzacego = nr_prowadzacego
        self.imie = imie
        self.nazwisko = nazwisko


class Kursy(db.Model):
    __tablename__ = 'kursy'

    nr_kursu = db.Column(db.Integer, unique = True, primary_key = True)
    nazwa = db.Column(db.String(255)) 
    nr_gl_prowadzacego = db.Column(db.Integer, db.ForeignKey('prowadzacy.nr_prowadzacego'))
    
    def __init__(self, nr_kursu, nazwa, nr_gl_prowadzacego):
        self.nr_kursu = nr_kursu
        self.nazwa = nazwa
        self.nr_gl_prowadzacego = nr_gl_prowadzacego






#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Studenci.query.all()

    return render_template("index.html", studia = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        imie = request.form['imie']
        nazwisko = request.form['nazwisko']


        my_data = Studenci(imie, nazwisko)
        db.session.add(my_data)
        db.session.commit()

        flash("Studenci chyba Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Studenci.query.get(request.form.get('id'))

        my_data.imie = request.form['imie']
        my_data.nazwisko = request.form['nazwisko']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Studenci.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)

