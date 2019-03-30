from flask import Flask
app = Flask(__name__)


# most basic example
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello'


# example using param variables
@app.route('/hello/<string:name>', methods=['GET'])
def say_hello(name):
    return 'Hello, {}'.format(name.title())
