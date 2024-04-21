#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Returns Hello HBNB """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Returns HBNB """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ Returns HBNB """
    vtext = text.replace('_', ' ')
    return 'C {}'.format(vtext)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """ Returns HBNB """
    vtext = text.replace('_', ' ')
    return 'Python {}'.format(vtext)


@app.route('/number/<int:n>', strict_slashes=False)
def n_number(n):
    """ Returns HBNB """
    return '{} is a number'.format(str(n))


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Returns HBNB """
    return render_template('5-number.html', n=str(n))


@app.route('/number_odd_or_even/<int:n>')
def odd_or_even(n):
    """ Returns HBNB """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
