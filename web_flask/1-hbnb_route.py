#!/usr/bin/python3
""" Module with script to start a Flask Web application """
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns:
            String Hello HBNB!
    """
    return ("Hello HBNB!")


@app.route('/hbnb')
def hbnb():
    """Returns
            HBNB
    """
    return ("HBNB")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
