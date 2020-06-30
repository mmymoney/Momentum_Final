"""
Routes and views for the flask application.
"""
import json
import urllib.request
import os
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from wtforms import Form, StringField, TextAreaField, validators, RadioField, SelectMultipleField, FloatField


from datetime import datetime, date
from flask import render_template, request, redirect, url_for
from FlaskAppAML import app

from FlaskAppAML.forms import SubmissionForm

# additional dependencies for API call to Rapid API (Yahoo Finance)
import requests
import math


# Our main app page/route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home():
    """Renders the home page which is the CNS of the web app currently, nothing pretty."""
    
    # Configuration for RDS instance
    mode="append"
    jdbc_url = "jdbc:postgresql://momentum-db.cgk0xpvhfuev.us-east-2.rds.amazonaws.com:5432/postgres"
    config = {"user":"root",
    "password": "rootroot",
    "driver":"org.postgresql.Driver"}

    form = SubmissionForm(request.form)

    #variable formation based on questionnaire submissions
    age = form.age.data
    email = form.email.data
    income_level = form.income_level.data
    sector_preference = form.sector_preference.data
    citizenship = form.citizenship.data
    education = form.education.data
    experience_years = form.experience_years.data
    periodicals = form.periodicals.data
    aspirations = form.aspirations.data
    diversification = form.diversification.data
    brokerage_acct = form.brokerage_acct.data
    interested_in_learning = form.interested_in_learning.data
    scenario_1 = form.scenario_1.data
    scenario_2 = form.scenario_2.data
    port_diversified = form.port_diversified.data
    safest_asset = form.safest_asset.data
    income_drawing = form.income_drawing.data
    fin_info = form.fin_info.data
    return_expectations = form.return_expectations.data
    normal_expectations = form.normal_expectations.data
    poor_expectations = form.poor_expectations.data
    three_yr_attitude = form.three_yr_attitude.data
    three_month_attitude = form.three_yr_attitude.data
    datetime_1 = datetime.now()

    # iterate and combine to string MultipleEntryField
    combined_periodicals = ""
    combined_aspirations = ""
    while len(periodicals)>0:
        combined_periodicals = periodicals[0] + ", " + combined_periodicals
        periodicals = np.delete(periodicals, 0)
    while len(aspirations)>0:
        combined_aspirations = aspirations[0] + ", " + combined_aspirations
        aspirations = np.delete(aspirations, 0)

    #form dataframe from submission data
    d = {'age': age, 'email': email, 'income_level': income_level, 'sector_preference': sector_preference, 
    'citizenship': citizenship, 'education': education, 'experience_years': experience_years, 'periodicals': combined_periodicals, 
    'aspirations': combined_aspirations, 'diversification': diversification, 'brokerage_acct': brokerage_acct, 
    'interested_in_learning': interested_in_learning, 'scenario_1': scenario_1, 'scenario_2': scenario_2, 
    'port_diversified': port_diversified, 'safest_asset': safest_asset, 'income_drawing': income_drawing, 
    'fin_info': fin_info, 'return_expectations': return_expectations, 'normal_expectations':normal_expectations, 
    'poor_expectations': poor_expectations, 'three_yr_attitude': three_yr_attitude, 
    'three_month_attitude': three_month_attitude, 'datetime': datetime_1}

    submission_df = pd.DataFrame(data = d, index = [0])
    
         
    # -------------------------------------------------------------------------------------------
    # from sqlalchemy import create_engine
    engine = create_engine('postgresql://root:rootroot@momentum-db.cgk0xpvhfuev.us-east-2.rds.amazonaws.com:5432/postgres')

    #use pandas to load questionnaire df into database
    submission_df.to_sql(name = 'questionnaire', con = engine, if_exists = 'append')
    # #query tables to validate load
    # pd.read_sql_query('select * from questionnaire', con=engine).head()

    # #timestamp conversion from user-submitted date
    # timestamp_t = str(int(datetime.strptime(form.Date.data , '%Y-%m-%d').timestamp())+86400)
    # timestamp_priordays = str(int(timestamp_t)-(86400*7))

    # #variables for call
    # url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    # querystring = {"frequency":"1d","filter":"history","period1":timestamp_priordays,"period2":timestamp_t,"symbol":"SPY"}

    # headers = {
    #     'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # #convert response variable to json format for slicing / variable assignment
    # response_json = response.json()

    # # feature set variables
    # open_t = response_json['prices'][0]['open']
    # high_t =  response_json['prices'][0]['high']
    # low_t =  response_json['prices'][0]['low']
    # close_t =  response_json['prices'][0]['close']
    # volume_t =  response_json['prices'][0]['volume']
    # t_3_volumediff =   response_json['prices'][3]['volume'] - response_json['prices'][0]['volume']
    # t_3_closediff =    response_json['prices'][3]['close'] - response_json['prices'][0]['close']
    # t_3_opendiff =    response_json['prices'][3]['open'] - response_json['prices'][0]['open']
    # t_2_volumediff = response_json['prices'][2]['volume'] - response_json['prices'][0]['volume']
    # t_2_closediff = response_json['prices'][2]['close'] - response_json['prices'][0]['close']
    # t_2_opendiff = response_json['prices'][2]['open'] - response_json['prices'][0]['open']
    # t_1_volumediff = response_json['prices'][1]['volume'] - response_json['prices'][0]['volume']
    # t_1_closediff = response_json['prices'][1]['close'] - response_json['prices'][0]['close']
    # t_1_opendiff = response_json['prices'][1]['open'] - response_json['prices'][0]['open']
    # pd_vert_delt = (response_json['prices'][0]['high']-response_json['prices'][0]['low'])/(response_json['prices'][1]['high']-response_json['prices'][1]['low'])
    # retracement_sig = (1-(high_t - close_t)/(high_t-low_t))
    # pd_deriv = -1*math.sin((close_t-open_t)/(response_json['prices'][1]['close']-response_json['prices'][1]['open']))

    # Form has been submitted
    if request.method == 'POST':

# -------------------------------------------------------------------------------------------
        # #summed column -jsean
        summed_df = submission_df.drop(columns=['email','sector_preference','periodicals'])
        summed_df['sum'] = summed_df.sum(axis=1)
        # #Return summed value as string - JOANA 
        # # there will always be only one item right?
        current_user_sum = summed_df['sum'].item()
        print(current_user_sum)
        # #current_user_agg = submission_df.loc[submission_df['email'] == email,'sum'].item()

        # #lower end = riskier | higher = safer
        # # The ETF recommendations made is not financial advice. ETF listing is pulled from yahoo Finanace equity screener based upon filters and parameters. 
        # # The following parameters were used to determine whether the ETF was high, medium, and low risk. Parameter: morningstar performance rating overall is 4-5 stars
        # #High Risk: Morningstar Risk Rating Overrrall (5 stars)
        etf_dictionary = {'Financial Sector':[('IYF','High'),('VFH','Medium'),('KRE','Low')],
                            'Technology Sector':[('FTEC','High'),('VGT','Medium'),('FDN','Low')],
                        'Utilities':[('RYU','High'),('YLCO','Medium'),('FUTY','Low')],
                        'Healthcare':[('FHLC','High'),('IHI','Medium'),('XHE','Low')],
                        'Energy':[('XLE','High'),('IEO','Medium'),('PXI','Low')],
                        'Consumer Staples':[('FSTA','High'),('VDC','Medium'),('IYK','Low')],
                        'Commodities':[('PDBC','High'),('DBC','Medium'),('GSG','Low')],
                        'Real Estate': [('MORT','High'),('FREL','Medium'),('VNQ','Low')],
                        'Government Bonds': [('AGG','High'),('AGG','Medium'),('AGG','Low')] }

        def chosen_etfs(user_agg,sector_chosen):
            for key,value in etf_dictionary.items():
                if sector_chosen == key:
                    if user_agg <= 35:
                        return value[0][0]
                    if user_agg <= 55:
                        return value[1][0]
                    else:
                        return value[2][0]

        current_etf = chosen_etfs(current_user_sum, sector_preference)
        global current_etf_global
        current_etf_global = current_etf
        
        # current_etf = chosen_etfs(65, 'Financial Sector')

        #yahoo api call
        import requests 
        import json

        #ETF: fiveYrAvgReturnPct, threeyearaverage,keystatics-ytdReturn, 
        #ETF: topholdings-sectorweightings, assetprofile-longBusinessSummary
        #BONDS: ALSO APPLICABLE
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"

        querystring = {"region":"US","lang":"en","symbol":current_etf}
        querystring2 = {"region": "US", "lang":"en","symbol":"AGG"}

        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
            }


        response = requests.request("GET", url, headers=headers, params=querystring)
        response_agg = requests.request("GET",url, headers=headers, params=querystring2)

        response_json_etf2 = response.json()
        response_agg = response_agg.json()

        three_yr = response_json_etf2['defaultKeyStatistics']['threeYearAverageReturn']['fmt']
        five_yr = response_json_etf2['defaultKeyStatistics']['fiveYearAverageReturn']['fmt']
        ytd_return = response_json_etf2['defaultKeyStatistics']['ytdReturn']['fmt']
        topholdings = response_json_etf2['topHoldings']['sectorWeightings']
        longbusinesssum = response_json_etf2['assetProfile']['longBusinessSummary']
       #AGG information
        three_yr_agg = response_agg['defaultKeyStatistics']['threeYearAverageReturn']['fmt']
        five_yr_agg = response_agg['defaultKeyStatistics']['fiveYearAverageReturn']['fmt']
        ytd_return_agg = response_agg['defaultKeyStatistics']['ytdReturn']['fmt']
        topholdings_agg = response_agg['topHoldings']['sectorWeightings']
        longbusinesssum_agg = response_agg['assetProfile']['longBusinessSummary']
        bondratings_bonds_agg = response_agg['topHoldings']['bondRatings']

        global three_yr_G, five_yr_G, ytd_return_G, topholdings_G,longbusinesssum_G, bondratings_bonds_G, three_yr_agg_G, five_yr_agg_G, ytd_return_agg_G, topholdings_agg_G, longbusinesssum_agg_G

        three_yr_G = three_yr
        five_yr_G = five_yr
        ytd_return_G = ytd_return
        topholdings_G = topholdings
        longbusinesssum_G = longbusinesssum
        bondratings_bonds_G = bondratings_bonds_agg
        three_yr_agg_G = three_yr_agg
        five_yr_agg_G = five_yr_agg
        ytd_return_agg_G = ytd_return_agg
        topholdings_agg_G = topholdings_agg
        longbusinesssum_agg_G = longbusinesssum_agg
        

        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
#         data =  {
#   "Inputs": {
#     "input1": {
#       "ColumnNames": [
#         "Open",
#         "High",
#         "Low",
#         "Close",
#         "Volume",
#         "T3_Vol_Diff",
#         "T3_Close_Diff",
#         "T3_Open_Diff",
#         "T2_Vol_Diff",
#         "T2_Close_Diff",
#         "T2_Open_Diff",
#         "T1_Vol_Diff",
#         "T1_Close_Diff",
#         "T1_Open_Diff",
#         "Prior_Day_Vert_Delta_Ratio",
#         "Retracement_Signal",
#         "Prior_Day_Derivative",
#         "T+1_Close",
#       ],
#       "Values": [
#         [
#             open_t,
#             high_t,
#             low_t,
#             close_t,
#             volume_t,
#             t_3_volumediff,
#             t_3_closediff,
#             t_3_opendiff,
#             t_2_volumediff,
#             t_2_closediff,
#             t_2_opendiff,
#             t_1_volumediff,
#             t_1_closediff,
#             t_1_opendiff,
#             pd_vert_delt,
#             retracement_sig,
#             pd_deriv,
#             ""
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
#         ]
#       ]
#     }
#   },
#   "GlobalParameters": {}
# }

#         # Serialize the input data into json string
#         body = str.encode(json.dumps(data))
# # str.encode
#         # Formulate the request
#         #req = urllib.request.Request(URL, body, HEADERS)
#         req = urllib.request.Request(Bayesian_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            # response = requests.post(URL, headers=HEADERS, data=body)
            # response = urllib.request.urlopen(req)
            # #print(response)
            # respdata = response.read()
            # result = json.loads(str(respdata, 'utf-8'))
            # result = do_something_pretty(result)
            # result = json.dumps(result, indent=4, sort_keys=True)
          # return render_template( 'final_result.html',title=, result=result)
               
                return redirect(url_for('secondresult'))
            
                
                    # result=result

            

        # An HTTP error
        except urllib.error.HTTPError as err:
           # result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
               # result=result
            )
            #print(err)

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year="2020",
        message='Demonstrating a website using Azure ML Api')

# Machine Learning Route


@app.route('/secondresult',methods=['GET','POST'])
def secondresult():

    form = SubmissionForm(request.form)
    etf_weight = form.etf_weighting.data
    bond_weight = form.bond_weighting.data
    energy_weight = form.energy_weighting.data
    tech_weight = form.tech_weighting.data
    util_weight = form.util_weighting.data
    fin_weight = form.fin_weighting.data
    health_weight = form.health_weighting.data
    constap_weight = form.constap_weighting.data
    condisc_weight = form.condisc_weighting.data
    energy_tick = form.energy_ticker.data
    tech_tick = form.tech_ticker.data
    util_tick = form.util_ticker.data
    fin_tick = form.fin_ticker.data
    health_tick = form.health_ticker.data
    constap_tick = form.constap_ticker.data
    condisc_tick = form.condisc_ticker.data
    datetime_1 = datetime.now()
    date_1 = date.today()
    
    #timestamp conversion from user-submitted date
    timestamp_t = str(int(datetime.strptime(str(date_1) , '%Y-%m-%d').timestamp()))

    timestamp_priordays = str(int(timestamp_t)-(86400*7))
#variables for call
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    # Financial (VFH ETF)
    querystring = {"frequency":"1d","filter":"history","period1":timestamp_priordays,"period2":timestamp_t,"symbol":"VFH"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #convert response variable to json format for slicing / variable assignment
    response_json = response.json()

    # feature set variables
    open_t = response_json['prices'][0]['open']
    high_t =  response_json['prices'][0]['high']
    low_t =  response_json['prices'][0]['low']
    close_t =  response_json['prices'][0]['close']
    adjclose_t =  response_json['prices'][0]['adjclose']
    volume_t =  response_json['prices'][0]['volume']
    t_1_closediff = response_json['prices'][1]['close'] - response_json['prices'][0]['close']


    if request.method == 'POST':
        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
            data =  {
    "Inputs": {
        "input1": {
        "ColumnNames": [
            # "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "T-1_Close_Diff",
            "T+30_Close"],
        "Values": [
            [
                # str(date_1),
                open_t,
                high_t,
                low_t,
                close_t,
                adjclose_t,
                volume_t,
                t_1_closediff,
                "0"]
            ]
        }
    },
    "GlobalParameters": {}
    }

            # Serialize the input data into json string
            body = str.encode(json.dumps(data))

            VFH_ML_KEY=os.environ.get('API_KEY', "8FErDr2F8XnmhbR0XscVKYRpgAC4R7E7yR9cIFyCAzpZavP0a1FaWQ9AV9qBvw7SYc8pNc7CfU9rS2oSI5AIgg==")
            VFH_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/171d5eadacbb47b5ab0811ef139f692b/execute?api-version=2.0&details=true")
            # Deployment environment variables defined on Azure (pull in with os.environ)

            # Construct the HTTP request header
            # HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}
            HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ VFH_ML_KEY)}

    # str.encode
            # Formulate the request
            #req = urllib.request.Request(URL, body, HEADERS)
            
            req = urllib.request.Request(VFH_URL, body, HEADERS)
            # Send this request to the AML service and render the results on page
            try:
               # response = requests.post(VFH_URL, headers=HEADERS, data=body)
                
                response = urllib.request.urlopen(req)
                #print(response)
                respdata = response.read()
                #print(respdata)
                result = json.loads(str(respdata, 'utf-8'))
                result = do_something_pretty(result)
                
                result = json.dumps(result, indent=4, sort_keys=True)
            
                return render_template (
                    'final_result.html',
                    title= 'The following prediction was made for the return of your portfolio:',
                    #result=result
                    result=result,
                )
        # An HTTP error
            except urllib.error.HTTPError as err:
                result="The request failed with status code: " + str(err.code)
                return render_template(
                    'final_result.html',
                    title='There was an error',
            # result=result
                )
                # result=result
            #----
            
    return render_template(
                'result.html',
                form=form,
                title="Your portfolio:",
                etf_content = longbusinesssum_G,
                etfg = current_etf_global,
                tyg = three_yr_G,
                fyg = five_yr_G,
                yrg = ytd_return_G,
                thg = topholdings_G,
                bragg_g = bondratings_bonds_G, 
                tyagg_g = three_yr_agg_G, 
                fyagg_g = five_yr_agg_G,
                yragg_g = ytd_return_agg_G,
                thagg_g = topholdings_agg_G, 
                lbsagg_g = longbusinesssum_agg_G, 
                

                )

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

    scored_label = value[8]
    
    # Convert values (a list) to a list of tuples [(cluster#,distance),...]
    # valuetuple = list(zip(range(valuelen-1), value[1:(valuelen)]))
    # Convert the list of tuples to one long list (flatten it)
    # valuelist = list(itertools.chain(*valuetuple))

    # Convert to a tuple for the list
    # data = tuple(list(value[0]) + valuelist)

    # Build a placeholder for the cluster#,distance values
    #repstr = '<tr><td>%d</td><td>%s</td></tr>' * (valuelen-1)
    # print(repstr)
    output_bayesian=f'Our linear regression model would predict a closing value of {str(round(float(scored_label),2))} USD for the 30th trading day following'
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output_bayesian
