#!/usr/bin/env python
from flask import Flask

app = Flask(__name__, static_url_path='/static')

@app.route('/hello')
def say_hello():
    return '<h1>You have reached the hello page</h1>'

@app.route('/')
def default_greet():
    return '<h1>Welcome to this dynamically created web server!</h1><p></p><img src="/static/acilogo.jpg" align="middle"></img>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)