#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 23:43:36 2018
"""

from flask import Flask, render_template
from flask_restful import Api, request
import json
from sklearn.externals import joblib

app = Flask("api-ml")
api = Api(app)

def check_key():
    retorno = {}
    
    api_key = request.headers.get('key')
    api_secret = request.headers.get('secret')

    retorno["output"] = "Autenticação com sucesso"
    retorno["result"] = True

    if not (api_key == "XFac-7m-7?CjphABgfyAYGAea2E_U7_qD8AP2-FW" and
        api_secret == "UQU8?5gmd+SgGPLtM&*B&x+R3s-4Z8bqAv+aZC6k"):
        retorno["output"] = "API Key ou API Secret inválidos"
        retorno["result"] = False

    return retorno

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World"

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route("/file", methods=["POST"])
def file():
    if "file" in request.files:
        f = request.files['file']
        f.save(f.filename)
    else:
        return "Arquivo não encontrado"
    return f.filename

@app.route("/predict", methods=["GET"])
def predict():
    retorno = {}

    lr_model_loaded = joblib.load('models/lr_model.pkl')

    if "temp_max" in request.args:
        temp_max = request.values["temp_max"]
    if "precipt" in request.args:
        precipt = request.values["precipt"]
    if "weekend" in request.args:
        weekend = request.values["weekend"]

    predict_value = [[int(temp_max), int(precipt), int(weekend)]]
    predicted = lr_model_loaded.predict(predict_value)

    retorno["output"] = "Predicted consumption successful for model " + request.values["model"]
    retorno["value"] = predicted[0]

    return json.dumps(retorno)

app.run(host="0.0.0.0", port=80, debug=True)