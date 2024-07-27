#!/usr/bin/python3
""" Module with script to start a Flask Web application """
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns:
            String Hello HBNB!
    """
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns
            HBNB
    """
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Replaces _ with space if text argument has it.
        Args:
            text (str) : Text to print
        Returns:
            C <text>
    """
    return (f"C {text.replace('_', ' ')}")


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_fun(text):
    """ Replaces _ with space if text argument has it.
        Args:
            text (str) : Text to print
        Returns:
            Python <text>
    """
    return (f"Python {text.replace('_', ' ')}")


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays text if n is an integer
        Args:
            n (int) : Number to display
        Returns:
            <n> is a number
    """
    return(f"{n} is a number")


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Renders templates to display integer
        Args:
            n (int) : Number to pass to template
        Returns:
            HTML file to render.
    """
    return (render_template('5-number.html', n=n))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
