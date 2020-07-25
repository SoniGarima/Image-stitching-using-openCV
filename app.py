import os
import sys
import numpy as np
import cv2
import json
import pandas as pd

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from util import base64_to_pil

# Declare a flask app
app = Flask(__name__)

def  model_predict():
    #.......open cv here


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        print(request.json)
        print('aaa')
        img1,img2 = base64_to_pil(request.json)

        preds = model_predict(img1,img2, model)
        type(preds)
        result=preds
        print(result)
        return jsonify(result)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
