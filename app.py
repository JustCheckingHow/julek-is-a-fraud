from flask import Flask, request, jsonify
from flask_cors import CORS

from modules import Scamwatcher, PolandCheck, AlexaRank

import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_record', methods=['GET'])
def get_rating():
    modules = [AlexaRank, Scamwatcher, PolandCheck]

    args = request.args
    name = args['name']

    res = {"name": name}
    for mod in modules:
        res.update(mod(name).return_data())

    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)
