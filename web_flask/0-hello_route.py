#!/usr/bin/python3
"""starts Flask web application"""


# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

from flask import Flask

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)   # Flask constructor

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route('/', strict_slashes=False)
# ‘/’ URL is bound with hello_hbnb() function.
def hello_hbnb():
    """returns Hello HBNB!"""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
