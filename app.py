from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from modules.ALEXA_RANK.alexa_rank import AlexaRank
from modules import Scamwatcher, WebpageResolver
from modules.WHO_IS.whois_api import WhoIs

import json

app = Flask(__name__)
CORS(app)
@app.errorhandler(404)

def not_found(e):
    return render_template('404.html')

@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/company.html')
def company():
    return render_template('company.html')

@app.route("/get_alexa", methods=['GET'])
def get_alexa():
    res = AlexaRank(request.args['name'].lower()).return_data()
    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)

@app.route("/get_scamwatcher", methods=['GET'])
def get_scamwatcher():
    res = Scamwatcher(request.args['name'].lower()).return_data()
    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)

@app.route("/get_webpage_resolver", methods=['GET'])
def get_WebpageResolver():
    res = WebpageResolver(request.args['name'].lower()).return_data()
    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)

@app.route("/get_whois", methods=['GET'])
def get_WhoIs():
    res = WhoIs(request.args['name'].lower()).return_data()
    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)

@app.route('/get_record', methods=['GET'])
def get_rating():
    modules = [AlexaRank, Scamwatcher, WebpageResolver, WhoIs]

    args = request.args
    name = args['name'].lower()

    res = {"name": name}
    for mod in modules:
        update = mod(name).return_data()
        res.update(update)

    res = {i: str(j) for i, j in res.items()}
    return jsonify(res)
