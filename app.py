import os
import sys
import numpy as np
import cv2
import json
import pandas as pd
import imutils
from imutils import paths

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from util import base64_to_pil
from util import np_to_base64
# Declare a flask app
app = Flask(__name__)

from IPython.display import Image 

def  model_predict(img1,img2):
    #.......open cv here
    # img1 = cv2.imread("images/s1.png")
    # img2 = cv2.imread("images/s2.png")
    
    img1=(np.array(img1))
    img2=(np.array(img2))
    
    if(len(img1.shape)==2):
        img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    
    if(len(img2.shape)==2):
        img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    
        
    images = [img1,img2]
    stitcher = cv2.Stitcher_create() 
    (status, stitched) = stitcher.stitch(images)
        
    stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
                cv2.BORDER_CONSTANT, (0, 0, 0))
    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    mask = np.zeros(thresh.shape, dtype="uint8")
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    minRect = mask.copy()
    sub = mask.copy()
    while cv2.countNonZero(sub) > 0:
        minRect = cv2.erode(minRect, None)
        sub = cv2.subtract(minRect, thresh)
        
    cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(c)
    stitched = stitched[y:y + h, x:x + w]
    # cv2.imwrite("output.png", stitched)
    return stitched



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img1,img2=base64_to_pil(request.json)
        img3=model_predict(img1,img2)
        img3=np_to_base64(img3)
        #return jsonify({'image_url': '/output.png'})
        return jsonify(img3)
    return None


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 4000), app)
    http_server.serve_forever()
