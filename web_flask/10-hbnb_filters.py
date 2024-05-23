#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
import models
from models import storage
from flask import render_template
from flask import Flask


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_list():
    """display a HTML page with the states listed in alphabetical order with cities"""
    states = storage.all("State").values()
    cities = storage.all("City").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', states=states, cities=cities, amenities=amenities)




@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')