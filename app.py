# Initial setup
from flask import Flask, request, redirect, url_for

import json
import requests
import time
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from sklearn.externals import joblib
import pandas as pd
import numpy as np
# Flask object creation
app = Flask(__name__)


# Index page
@app.route("/")
def index():
    return_value = {"message": "Welcome to the Notify-IPL API!"}
    json_string = json.dumps(return_value)
    return json_string

'''@app.route('/predict', methods=['POST'])'''
@app.route('/predict', methods=['GET'])
def predict():
     json_ = request.json
     myvar = request.args["myvar"]
     print(myvar[0])
     temp = myvar.split(',')
     inputarray = []
     for item in temp:
         inputarray.append(float(item))
     print(inputarray)
     #query_df = pd.DataFrame(json_)
     #query = pd.get_dummies(query_df)
     #inputarray = np.array([[411.0,417.0,6.0,417.0,411.0,417.0,414.54,2.95,8.71,-1.87,-0.37]])
     #input_query - np.array([[411.0,417.0,6.0,417.0,411.0,417.0,414.54,2.95,8.71,-1.87,-0.37]])
     clf = joblib.load('model.pkl')
     prediction = clf.predict([inputarray])
     percentage_predictions = clf.predict_proba([inputarray])
     #print(type(percentage_predictions))
     percentage_predictions = np.array(percentage_predictions.tolist())
     print(percentage_predictions[0][0])
     return jsonify({'prediction': list(prediction),'ceremics':percentage_predictions[0][0],'paper':percentage_predictions[0][1]})


# Help page
@app.route("/help")
def help():
    return_value = {"message": "The available commands for this API will be visible here :)"}

    json_string = json.dumps(return_value)

    return json_string


# Error page
@app.errorhandler(404)
def page_not_found(e):
    return json.dumps("error"), 404


if __name__ == "__main__":
    app.debug = True
    clf = joblib.load('model.pkl')
    app.run()
