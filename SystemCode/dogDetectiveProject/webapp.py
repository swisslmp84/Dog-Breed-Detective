import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
import numpy as np
import pandas as pd

from keras.models import load_model
from util.predictBreed import predict_image
from util.getDogInfo import getDogInfo
from util.getDogRecommendation import filterCleanDataset, normalize, getDogRecommendation

UPLOAD_FOLDER = './static/uploads/'
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.featureExtractor = load_model('./models/feature_extractor.h5')
app.dnn = load_model('./models/dogbreed.h5')

@app.route('/')
def index_form():
	return render_template('index.html')

@app.route('/uploadImage', methods=['POST'])
def predictBreed():
	return predict_image(request, app.featureExtractor, app.dnn)

@app.route('/dogInfo', methods=['GET'])
def dogInfo():
	return getDogInfo(request)

@app.route('/dogRecommendation', methods=['GET'])
def dogRecommendation():
	return getDogRecommendation(request)
        
if __name__ == "__main__":
	app.run(host= '0.0.0.0', port=8080)


