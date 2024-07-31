#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states: HTML page with a list of all State objects.
    /states/<id>: HTML page displaying the given state with <id>.
"""
from models import storage
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)

# Determine the type of storafge being used
storage_type = getenv('HBNB_TYPE_STORAGE')


@app.route("/states", strict_slashes=False)
def states():
    """Displays an HTML page with a list of all States.

    States are sorted by name.
    """
    states = storage.all("State").values()
    states = sorted(states, key=lambda x: x.name)
    return render_template("9-states.html", states=states, cities=None)


@app.route("/states/<id>", strict_slashes=False)
def state_cities(id):
    """Displays an HTML page with the cities of a specific state or
    'Not found! if not found"""
    state = None
    for s in storage.all("State").values():
        if s.id == id:
            state = s
            break

    if state:
        print(f"Found state: {state.name}, ID: {state.id}")
        if storage_type == 'db':
            cities = sorted(state.cities, key=lambda x: x.name)
        else:
            cities = sorted(state.cities(), key=lambda x: x.name)
        print(f"Cities: {cities}")
        return render_template('9-states.html', states=[state], cities=cities)
    else:
        print("State not found!")
        return render_template('9-states.html', states=[], cities=None,
                               not_found=True)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
