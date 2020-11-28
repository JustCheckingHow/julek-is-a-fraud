from flask import Flask, request
from flask_cors import CORS

from modules.ALEXA_RANK.alexa_rank import AlexaRank

import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_record', methods=['GET'])
def get_rating():
    args = request.args
    name = args['name']
    alexa_rank = AlexaRank(name).return_data()['AlexaRank']
    print(alexa_rank)

    return """{
        'name': '""" + name + """',
        'tax_residence': ['Polska', 'Wyspy Owcze'],
        'alexa_rank': '""" + alexa_rank + """',
        'google_rank': '42',
        'license': 'true',
        'number': '777 666 555',
        'is_number_scam': 'true',
        'is_polish': 'true',
        'score': '57',
        'is_rebrand': 'true',
        'previous_brands': ['Aaaa', 'Bbbb']
    }"""
