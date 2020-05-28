"""
Routes and views for the flask application.
"""
import json
import urllib.request
import os

from datetime import datetime
from flask import render_template, request, redirect
from FlaskAppAML import app

from FlaskAppAML.forms import SubmissionForm

# additional dependencies for API call to Rapid API (Yahoo Finance)
import requests

import math



Bayesian_ML_KEY=os.environ.get('API_KEY', "6LgM3hobpFQkecNPOBz2QRHvSIzYJLdQBfahZtC49sPMjiOwIiNMAAtALXDNuZK1zE3DTzsKoJB4yvfZkSmDTQ==")
Bayesian_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/00d11b98f56946f286a640541b35f9ec/execute?api-version=2.0&details=true")
# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header
# HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}

HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ Bayesian_ML_KEY)}

# Our main app page/route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page which is the CNS of the web app currently, nothing pretty."""

    form = SubmissionForm(request.form)

    #timestamp conversion from user-submitted date
    timestamp_t = str(int(datetime.strptime(form.Date.data , '%Y-%m-%d').timestamp())+86400)
    timestamp_priordays = str(int(timestamp_t)-(86400*7))

    #variables for call
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    querystring = {"frequency":"1d","filter":"history","period1":timestamp_priordays,"period2":timestamp_t,"symbol":"SPY"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #convert response variable to json format for slicing / variable assignment
    response_json = response.json()

    #feature set variables
    open_t = response_json['prices'][0]['open']
    high_t =  response_json['prices'][0]['high']
    low_t =  response_json['prices'][0]['low']
    close_t =  response_json['prices'][0]['close']
    volume_t =  response_json['prices'][0]['volume']
    t_3_volumediff =   response_json['prices'][3]['volume'] - response_json['prices'][0]['volume']
    t_3_closediff =    response_json['prices'][3]['close'] - response_json['prices'][0]['close']
    t_3_opendiff =    response_json['prices'][3]['open'] - response_json['prices'][0]['open']
    t_2_volumediff = response_json['prices'][2]['volume'] - response_json['prices'][0]['volume']
    t_2_closediff = response_json['prices'][2]['close'] - response_json['prices'][0]['close']
    t_2_opendiff = response_json['prices'][2]['open'] - response_json['prices'][0]['open']
    t_1_volumediff = response_json['prices'][1]['volume'] - response_json['prices'][0]['volume']
    t_1_closediff = response_json['prices'][1]['close'] - response_json['prices'][0]['close']
    t_1_opendiff = response_json['prices'][1]['open'] - response_json['prices'][0]['open']
    pd_vert_delt = (response_json['prices'][0]['high']-response_json['prices'][0]['low'])/(response_json['prices'][1]['high']-response_json['prices'][1]['low'])
    retracement_sig = (1-(high_t - close_t)/(high_t-low_t))
    pd_deriv = -1*math.sin((close_t-open_t)/(response_json['prices'][1]['close']-response_json['prices'][1]['open']))

    # Form has been submitted
    if request.method == 'POST' and form.validate():

        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
        data =  {
  "Inputs": {
    "input1": {
      "ColumnNames": [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "T3_Vol_Diff",
        "T3_Close_Diff",
        "T3_Open_Diff",
        "T2_Vol_Diff",
        "T2_Close_Diff",
        "T2_Open_Diff",
        "T1_Vol_Diff",
        "T1_Close_Diff",
        "T1_Open_Diff",
        "Prior_Day_Vert_Delta_Ratio",
        "Retracement_Signal",
        "Prior_Day_Derivative",
        "T+1_Close",
      ],
      "Values": [
        [
            open_t,
            high_t,
            low_t,
            close_t,
            volume_t,
            t_3_volumediff,
            t_3_closediff,
            t_3_opendiff,
            t_2_volumediff,
            t_2_closediff,
            t_2_opendiff,
            t_1_volumediff,
            t_1_closediff,
            t_1_opendiff,
            pd_vert_delt,
            retracement_sig,
            pd_deriv,
            ""
        #   form.Open.data,
        #   form.High.data,
        #   form.Low.data,
        #   form.Close.data,
        #   form.Volume.data,
        #   form.T3_Vol_Diff.data,
        #   form.T3_Close_Diff.data,
        #   form.T3_Open_Diff.data,
        #   form.T2_Vol_Diff.data,
        #   form.T2_Close_Diff.data,
        #   form.T2_Open_Diff.data,
        #   form.T1_Vol_Diff.data,
        #   form.T1_Close_Diff.data,
        #   form.T1_Open_Diff.data,
        #   form.Prior_Day_Vert_Delta_Ratio.data,
        #   form.Retracement_Signal.data,
        #   form.Prior_Day_Derivative.data,
        #   ""
        ]
      ]
    }
  },
  "GlobalParameters": {}
}

        # Serialize the input data into json string
        body = str.encode(json.dumps(data))
# str.encode
        # Formulate the request
        #req = urllib.request.Request(URL, body, HEADERS)
        req = urllib.request.Request(Bayesian_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            # response = requests.post(URL, headers=HEADERS, data=body)
            response = urllib.request.urlopen(req)
            #print(response)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = do_something_pretty(result)
            # result = json.dumps(result, indent=4, sort_keys=True)
            return render_template(
                'result.html',
                title="This is the result from AzureML running our example T+1 Prediction:",
                result=result)

        # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
                result=result)
            #print(err)

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year="2020",
        message='Demonstrating a website using Azure ML Api')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year="2020",
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Tools',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/lstm2')
def lstm2():
    """Renders the LSTM page."""
    return render_template(
        'lstm2.html',
        title='LSTM',
        year="2020",
        message='Your LSTM page.'
    )

@app.route('/tableau')
def tableau():
    """Renders the LSTM page."""
    return render_template(
        'tableau.html',
        title='Market Data',
        year="2020",
        message='Your market data page.'
    )

def do_something_pretty(jsondata):
    
    form = SubmissionForm(request.form)
    """We want to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    # We only want the first array from the array of arrays under "Value" 
    # - it's cluster assignment and distances from all centroid centers from k-means model
    value = jsondata["Results"]["output1"]["value"]["Values"][0]
    # valuelen = len(value)
    print(value)

    scored_label = value[18]
    
    # Convert values (a list) to a list of tuples [(cluster#,distance),...]
    # valuetuple = list(zip(range(valuelen-1), value[1:(valuelen)]))
    # Convert the list of tuples to one long list (flatten it)
    # valuelist = list(itertools.chain(*valuetuple))

    # Convert to a tuple for the list
    # data = tuple(list(value[0]) + valuelist)

    # Build a placeholder for the cluster#,distance values
    #repstr = '<tr><td>%d</td><td>%s</td></tr>' * (valuelen-1)
    # print(repstr)
    output_bayesian=f'Our linear regression model would predict a closing value of {str(round((float(scored_label)*294.433746 + 43.90625),2))} USD for the trading day following {form.Date.data}'
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output_bayesian
