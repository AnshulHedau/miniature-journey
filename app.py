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
import numpy as np,scipy.stats
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
     clf = joblib.load('model.pkl')
     myvar = request.args["myvar"]
     parameter_list = myvar.split(',')
     myvar = parameter_list[0]
     upper_value = int(parameter_list[1])
     lower_value = int(parameter_list[2])
     print(myvar)
     len_array = len(myvar)
     list_filtered_values = []
     for i in range(0,len_array):
         if (myvar[i] == '0'):
             list_filtered_values.append(lower_value)
         else:
             list_filtered_values.append(upper_value)
     #temp = myvar.split(',')
     print(list_filtered_values)
     inputarray = []
     inputarray.append([np.amin(list_filtered_values),np.amax(list_filtered_values),np.ptp(list_filtered_values),
                           np.percentile(list_filtered_values,75),np.percentile(list_filtered_values,25),
                           np.median(list_filtered_values),np.mean(list_filtered_values),np.std(list_filtered_values),
                           np.var(list_filtered_values),scipy.stats.kurtosis(list_filtered_values),
                           scipy.stats.skew(list_filtered_values)])
     print(inputarray)
     #query_df = pd.DataFrame(json_)
     #query = pd.get_dummies(query_df)
     prediction = clf.predict(inputarray)
     percentage_predictions = clf.predict_proba(inputarray)
     #print(type(percentage_predictions))
     percentage_predictions = np.array(percentage_predictions.tolist())
     print(percentage_predictions[0][0])
     return jsonify({'prediction': list(prediction),'ceremics':percentage_predictions[0][0],'paper':percentage_predictions[0][1],'wood':0,'metal':0})


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
