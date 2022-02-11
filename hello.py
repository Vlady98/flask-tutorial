from crypt import methods
from flask import Flask, jsonify, request
from models.country import countries

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

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


if __name__ == '__main__':

    app.run(debug=True)