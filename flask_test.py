from flask import Flask, render_template, request
from urllib import parse
import os
import json
app = Flask(__name__)

@app.route('/')
def Form():
    return render_template('index.html')

@app.route('/flask_test.py', methods=['POST'])
def whatwever():
    with open("food.json", "w") as json_file:
        json.dump(request.args, json_file)
    return request.args

@app.route('/flask_test.py', methods=['GET'])
def new():
    return "using get"

if __name__ == '__main__':
    app.run()
