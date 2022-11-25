#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "xsc0DgO5B50sSt04GVW3Lnrcm1Bou0Bn9oFqlEK7g01N"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



#model = pickle.load(open('model.pkl', 'rb'))
#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
def man():
    return flask.render_template('form.html')
    

@app.route('/predict',methods = ['POST'])
def home():
    x=[param for param in request.form.values()]  
    x=[float(p) for p in x[2:]]
    print(x)  
    lis = [['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
       'red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria',
       'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
       'potassium', 'hemoglobin', 'packed_cell_volume',
       'white_blood_cell_count', 'red_blood_cell_count', 'hypertension',
       'diabetesmellitus', 'coronary_artery_disease', 'appetite','pedal_edema','anemia']]
    payload_scoring = {"input_data": [{"fields": lis, "values": x}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f4af460b-49e4-4b53-9c7a-25929a2729b8/predictions?version=2022-11-24', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    
    pred = response_scoring.json() 
    p = pred['predictions'][0]['values'][0][0]
    
    print(p)
    return render_template('result.html', data=p)
    
if __name__ == "__main__":
	app.run(debug=True)