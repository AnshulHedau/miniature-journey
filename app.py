# Initial setup
from flask import Flask, request, redirect, url_for

import json
import requests
import time
import re
import pyrebase
import keras
import tensorflow as tf
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from sklearn.externals import joblib
import pandas as pd
import numpy as np,scipy.stats

from keras.models import load_model
# Flask object creation
app = Flask(__name__)


# Index page
@app.route("/")
def index():
    return_value = {"message": "Welcome to the Miniature Journey API!"}
    json_string = json.dumps(return_value)
    return json_string

'''@app.route('/predict', methods=['POST'])'''
@app.route('/predict')
def predict():
     json_ = request.json
     model = load_model("my_model.h5")
     config = {
         "apiKey": "AIzaSyDNthbeIvXGp5AkpiHA2yMmH5SJ8ww75CQ",
         "authDomain": "lien-1553715274263.firebaseapp.com",
         "databaseURL": "https://lien-1553715274263.firebaseio.com",
         "storageBucket": "lien-1553715274263.appspot.com"
     }

     firebase = pyrebase.initialize_app(config)
     fb_database = firebase.database()

     stored_data = fb_database.child('car_data').get().val()
     z_gyro = []
     mean_gyro = [-0.10162200279091103]
     for key, value in stored_data.items():
         if (len(value) > 4):
             z_gyro.append(value['gyro_z'])
             mean_gyro = [value['gyro_z']]
         else:
             z_gyro.append(mean_gyro[0])

     z_gyro = z_gyro[-25:]
     test_gyro = []
     test_gyro.append(z_gyro)
     test_gyro = np.array(test_gyro)
     print(len(test_gyro[0]))
     result_test = model.predict([test_gyro])

     if (result_test[0][1] > result_test[0][0]):
         print("Rash")
     else:
         print("Normal")

     return_value = {"message": "Welcome to the Miniature Journey API!"}
     json_string = json.dumps(return_value)
     return json_string

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
    app.run()
