from crypt import methods
from ensurepip import bootstrap
from locale import DAY_1
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from models.country import countries
from flask import make_response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
        

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
        form=form, name=session.get('name'),
        known=session.get('known', False))  

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/country')
def getCountries():
    return jsonify({"data": countries, "message": "List of countries", "status": "succesful"})


@app.route('/country/<string:country_name>')
def getCountry(country_name):
    countryGET = [country for country in countries if country['name'] == country_name]

    if len(countryGET) > 0:

        return jsonify({"data": countryGET, "message": "Country found", "status": "succesful"})

    else:

        return jsonify({"data": countryGET, "message": "No data", "status": "error"})


@app.route('/country', methods=['POST'])
def addCountry():

    newCountry = {
        "name": request.json['name'],
        "capital": request.json['capital'],
        "population": request.json['population'],
    }
        
    countries.append(newCountry)
    
    return jsonify({"data": countries, "message": "Country added", "status": "succesful"})


@app.route('/country/<string:country_name>', methods=['PUT'])
def editCountry(country_name):

    countryGET = [country for country in countries if country['name'] == country_name]

    if (len(countryGET) > 0):

        countryGET[0]['name'] = request.json['name']
        countryGET[0]['capital'] = request.json['capital']
        countryGET[0]['population'] = request.json['population']
    
        return jsonify({"data": countryGET[0], "message": "Country edited", "status": "succesful"})
    
    else:

        return jsonify({"data": countryGET, "message": "No data", "status": "error"})


@app.route('/country/<string:country_name>', methods=['DELETE'])
def deleteCountry(country_name):

    countryGET = [country for country in countries if country['name'] == country_name]

    if (len(countryGET) > 0):

        countries.remove(countryGET[0])
    
        return jsonify({"data": countries, "message": "Country deleted", "status": "succesful"})
    
    else:

        return jsonify({"data": countryGET, "message": "Item not found", "status": "error"})

class NameForm(FlaskForm):

    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


if __name__ == '__main__':

    # app.run(debug=False)   #modo sin debug mode, descomentar al ponerlo en PRODUCCION
    app.run(debug=True) #cuando el debug=True, se reinicia constantemente para revisar cambios, QUITAR EN PRODUCCION DEBUG MODE