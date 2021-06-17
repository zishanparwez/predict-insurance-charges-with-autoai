from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIxMDUyMDE4MzYiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjMwMDIzNkE4IiwiaWQiOiJJQk1pZC02NjMwMDIzNkE4IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMmI3ZjY0YTItYmRlNS00NDk3LTliODQtMTZhNWNkMGY4M2U5IiwiaWRlbnRpZmllciI6IjY2MzAwMjM2QTgiLCJnaXZlbl9uYW1lIjoiWmlzaGFuIiwiZmFtaWx5X25hbWUiOiJQYXJ3ZXoiLCJuYW1lIjoiWmlzaGFuIFBhcndleiIsImVtYWlsIjoiemlzaGFucGFyd2V6Nzg2QGdtYWlsLmNvbSIsInN1YiI6Inppc2hhbnBhcndlejc4NkBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJ6aXNoYW5wYXJ3ZXo3ODZAZ21haWwuY29tIiwiaWFtX2lkIjoiaWFtLTY2MzAwMjM2QTgiLCJuYW1lIjoiWmlzaGFuIFBhcndleiIsImdpdmVuX25hbWUiOiJaaXNoYW4iLCJmYW1pbHlfbmFtZSI6IlBhcndleiIsImVtYWlsIjoiemlzaGFucGFyd2V6Nzg2QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6ImZjYTliNzAzZDFmOTRlMzJhY2ZlY2RkMjBiNjRhNzczIiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjIzOTU0MzE0LCJleHAiOjE2MjM5NTc5MTQsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vb2lkYy90b2tlbiIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.cCBdTt4iPvK-xl8fNnIfFoXeI7mVRPJGFAyufSWMYVrNuraFAEffBQMr_GsVbnqAGqFZT7GigKjccxp_3QCX2dwemiicTU01wZ14rH3wuXqUMTKchN-zRiIfyHWZP3Z7DbgqXF67rqDxtXVROMG-sXsf-Do9sSmMSC0mFxqW8DQ9ZNxSysTgkBUg7jhfS8AHXtW6OBF2hzMLKhArIfnMHCi7tFNKBM-pD4bns56IXwDsqxxf-UCKRKym33CoSOioRweKq4GMfhyxREhxfqljHTE9vcXzoUPvS4ZVoeW761uQqRC_W4G3tSlkVW1XBaVosqCzQCFVPHrVG71-U6TJBg"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}
          
        response_scoring = requests.post("https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/0bdff7e8-99a9-4bd0-83e4-17e51bb02dcd/predictions?version=2021-06-17", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)