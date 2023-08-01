from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Commander Store</h1>'


@app.route('/about')
def about():
    return '<h1>About Page</h1> </br> <p> This is the about page </p>'
