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
        # topholdings = response_json_etf2['topHoldings']['sectorWeightings']
        longbusinesssum = response_json_etf2['assetProfile']['longBusinessSummary']
       
        #AGG information
        three_yr_agg = response_agg['defaultKeyStatistics']['threeYearAverageReturn']['fmt']
        five_yr_agg = response_agg['defaultKeyStatistics']['fiveYearAverageReturn']['fmt']
        ytd_return_agg = response_agg['defaultKeyStatistics']['ytdReturn']['fmt']
        
        longbusinesssum_agg = response_agg['assetProfile']['longBusinessSummary']
        # bondratings_bonds_agg = response_agg['topHoldings']['bondRatings']
   
        
        global three_yr_G, five_yr_G, ytd_return_G, topholdings_G,longbusinesssum_G, bondratings_bonds_G, three_yr_agg_G, five_yr_agg_G, ytd_return_agg_G, topholdings_agg_G, longbusinesssum_agg_G
        
        three_yr_G = three_yr
        five_yr_G = five_yr
        ytd_return_G = ytd_return
        # topholdings_G = topholdings
        longbusinesssum_G = longbusinesssum
        # bondratings_bonds_G = bondratings_bonds_agg
        three_yr_agg_G = three_yr_agg
        five_yr_agg_G = five_yr_agg
        ytd_return_agg_G = ytd_return_agg
        longbusinesssum_agg_G = longbusinesssum_agg
        
        

        # Send this request to the AML service and render the results on page
        try:

                return redirect(url_for('secondresult'))
            
        # An HTTP error
        except urllib.error.HTTPError as err:
           # result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
               
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
    
    weights_chosen = [etf_weight,bond_weight,energy_weight,tech_weight,util_weight,fin_weight,health_weight,constap_weight,condisc_weight]
    tickers_chosen = [energy_tick,tech_tick,util_tick,fin_tick,health_tick,constap_tick,condisc_tick]
    #timestamp conversion from user-submitted date
    timestamp_t = str(int(datetime.strptime(str(date_1) , '%Y-%m-%d').timestamp()))

    timestamp_priordays = str(int(timestamp_t)-(86400*7))
#variables for call
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    # Financial (VFH ETF)
    etf_tickers = ['VFH','VGT','YLCO','IHI','IEO','VDC','DBC','FREL','AGG','IYF','KRE','FTEC','FDN','RYU','FUTY','FHLC','XHE','XLE','PXI','FSTA','IYK','PDBC','GSG','MORT','VNQ']
    etf_attr_list = []
    for i in etf_tickers:
        single_etf = []
        querystring = {"frequency":"1d","filter":"history","period1":timestamp_priordays,"period2":timestamp_t,"symbol": i}

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
        single_etf.extend((open_t, high_t, low_t, close_t, adjclose_t, volume_t, t_1_closediff))
        etf_attr_list.append(single_etf)

        global closing_price
        closing_price = close_t

    if request.method == 'POST':
        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
        body_list = []
        for i in etf_attr_list:

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
                    i[0],
                    i[1],
                    i[2],
                    i[3],
                    i[4],
                    i[5],
                    i[6],
                    "0"]
                ]
            }
        },
        "GlobalParameters": {}
        }
            # Serialize the input data into json string
            body = str.encode(json.dumps(data))
            body_list.append(body)

        VFH_ML_KEY=os.environ.get('API_KEY', "8FErDr2F8XnmhbR0XscVKYRpgAC4R7E7yR9cIFyCAzpZavP0a1FaWQ9AV9qBvw7SYc8pNc7CfU9rS2oSI5AIgg==")
        VFH_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/171d5eadacbb47b5ab0811ef139f692b/execute?api-version=2.0&details=true")
        # Deployment environment variables defined on Azure (pull in with os.environ)
        VGT_ML_KEY = os.environ.get('API_KEY', "3BgDbPsWBJQ8+a3i9kXiSYRCjJuYZ97IIqbfT/gjWbNYixGdlKWiJvN6OvEYY2brXFhYSDshlNUJCtf8kc7REg==")
        VGT_URL = os.environ.get ('URL',"https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/467d867f6dbd4f70b1015b2eb21eab4b/execute?api-version=2.0&details=true")

        YLCO_ML_KEY = os.environ.get ('API_KEY',"czcrAnbVlR+GrpAFatQNuFD0HOQuWnU+9mXSZC1XJR+UF+zYJiDce9fysiiGe90bO4wTrtWa45BV6bEJgbeTmg==")
        YLCO_URL = os.environ.get ('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/bf2d38a37d9a4c919f963e9df662c35e/execute?api-version=2.0&details=true")

        IHI_ML_KEY = os.environ.get('API_KEY', "brT8wq3oF7SVXiHd0gFqiRTxnFygqVBNujs21JJ6HFHhqjKfVhoUbCzIfopC/g5JLc5jeDrEcVbr5GdvnATVTQ==")
        IHI_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/ce7d321e9e7240c0bc2e11dfae547a18/execute?api-version=2.0&details=true")

        IEO_ML_KEY = os.environ.get('API_KEY',"IvZHJcesvOSHNzGmB++orqv4B2ivf2fqchqOx4A6ATL61AfJquyVzb9LYpySQFD2vYIvoCqM5jIYgzYPV47l0w==")
        IEO_URL = os.environ.get('URL',"https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/7a32eb19edfa49768b38be1b00778a5c/execute?api-version=2.0&details=true")

        VDC_ML_KEY = os.environ.get('API_KEY', "oSd5LHaVAmDJOoUIE04hXaZLJ2lbHoaNIkCXUeAdAT4CZzhfl/rRh0geSzAU3FrXRLVuDAMTyjgHOhfsv1dYAA==")
        VDC_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/dc4ab8189fd84a7085062076e4ba12a2/execute?api-version=2.0&details=true")

        DBC_ML_KEY = os.environ.get('API_KEY', "TJH8ueT5rjb3JQN962ytyrRvuPECX2IIUBpN+xUMZwcqfaKxvwlRXXnpcwF/z64Ret1edLO79NjYIFWbsG2lbQ==")
        DBC_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/99b436f2f83c4db693fdd3351d109fbe/execute?api-version=2.0&details=true")

        FREL_ML_KEY = os.environ.get('API_KEY', "2GMc3n+xQoK+2Nie+jiTXANIMxRzXT8U5T/IYFQIeY7mJVH+jYwmc3FPETEMMBqHQmjTzF8gbHgM8E0gbdAoTg==")
        FREL_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/0cf918761a0245df91c9df109ac8ead8/execute?api-version=2.0&details=true")

        AGG_ML_KEY = os.environ.get("API_KEY", "99n5TXjg/US+B8iKuUikp7AMoYO81Ak3Umq6xzraiwMeKPRrByEl3bQhNFGMxWY/eeg4f7hUSUGjEHv4nvEM6Q==")
        AGG_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/2402bd9da1eb40c2a90551198b4d209d/execute?api-version=2.0&details=true")

        IYF_ML_KEY = os.environ.get("API_KEY", "+0PZ4Do44hDEPRIiMrZMBIz1A5OoaetZqMLWrHYwXoq78AgyG2mk+ZNjqynH8G25aR2TwP1bvgPWcnPYEVEWGw==")
        IYF_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/b37ee96356a54c44a0cb7bc96390cce1/execute?api-version=2.0&details=true")

        KRE_ML_KEY = os.environ.get("API_KEY", "JP9KQOeG6nzgikEm3jZFB+SKVJAcwbDzBWLUcO5WsbDom2d2gr0//LlQoKOvmmwg5ZjAs+4wj/TKDupRVG8p3w==")
        KRE_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/7778b0ee5a714a6292711988618e45ce/execute?api-version=2.0&details=true")

        FTEC_ML_KEY = os.environ.get("API_KEY", "2kupaA1PW5SkfRl49IeapOnLFgVFyA7QswqxJ/be9HF4hBJwx8wNkflplB8H4x5xW/Mit4knheqNSA1SQhtjnQ==")
        FTEC_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/df47509c0f7b4c809a7e3098cabea7e8/execute?api-version=2.0&details=true")

        FDN_ML_KEY = os.environ.get("API_KEY", "kalqSeYcT03ac7+Y0yorrdSEvQ82s5q4pzONeLabw150VEHqzYkvPN55FbYbBpuytgJCnhflleJx1Wjqx9Y+0g==")
        FDN_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/f9056118871c4016b64df3ff306ea6d0/execute?api-version=2.0&details=true")

        RYU_ML_KEY = os.environ.get("API_KEY", "x6sXZgP4Z60ihwBpuum5pk4B2n5nKkRMAA4i6G6BZ4Ju7z7LLNPdbkWfdStOburjAvRrLPN3F0jsyFQfwpaiOA==")
        RYU_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/673eab634e9a43bab8bd916293f1b0fe/execute?api-version=2.0&details=true")

        FUTY_ML_KEY = os.environ.get("API_KEY", "rFkaSEiOg5LU1ODHMy9+ObnBmg/tdngaFgNosGCEKVQRMBIcr71ZKM5hd1iEBc62qO6qLoWrIzyy1ghXEgTheA==")
        FUTY_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/e8d9b311444e43bab767e1b37d814e73/execute?api-version=2.0&details=true")

        FHLC_ML_KEY = os.environ.get("API_KEY", "FgtA+3/f3MwNUBbrdkOMvbKEoKk5uTxXk2bzVhiAMEbffGnL2TFj3loNFkeY7up7n6m5U9+WUmCVQS2RgWurGQ==")
        FHLC_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/7bc24f3c6a724311aa2b9fe9aac3b072/execute?api-version=2.0&details=true")

        XHE_ML_KEY = os.environ.get("API_KEY", "pgZCaps937cjlFeCAORzoOKPrYvNkjnJBRrB78nnwly8kHJs5xa9oEaZ9eS9x2MIVAPf/pi/xZcdg1QUVkkJnQ==")
        XHE_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/f2e083369a9b444e8ad87bdcac6de097/execute?api-version=2.0&details=true")

        XLE_ML_KEY = os.environ.get("API_KEY", "qUqVTIcPCI1GPOWJb0vomlJUAXsHIfmxRgzeUYV0XRkYMm4AoIOGMzzYiPrwgehYyJn9nkb8bFtnQO05cub/TQ==")
        XLE_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/93c8c6280f4843738eb0f3ae63b1fbfc/execute?api-version=2.0&details=true")

        PXI_ML_KEY = os.environ.get("API_KEY", "jtEp8rzvtY3jyCoGs2swh/FGJ7iU5PhDhb54+9EIqfuckZEN7cjtC4hlOEQhNmIzAMi4VH7g7kZ3FyG8y75xXw==")
        PXI_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/2b0d8f6af1024e90a9e62b297a1f9b75/execute?api-version=2.0&details=true")

        FSTA_ML_KEY = os.environ.get("API_KEY", "Vl6kPEZ4fUbZYIUl5uHUYPsjieZeg7AujcweePGQhGdOSZV0cpjtrVbcfqg/DeBjDwgF401sDUKPljQuAfWIcw==")
        FSTA_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/36f73752487041209c2f85210bbdcb1b/execute?api-version=2.0&details=true")

        IYK_ML_KEY = os.environ.get("API_KEY", "4UNxbiK9mauO+/VRpMPSjxa7FR30M98Mkcl0qCE6waS+azVCsGCALIk9Dp8TF2bdeQYvByXpK25a5N7D7NKDpQ==")
        IYK_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/555cc9684b404539b26e51bf9714c049/execute?api-version=2.0&details=true")

        PDBC_ML_KEY = os.environ.get("API_KEY", "iLpxmDXQr5AuCHA5fCcWcLNk0cDz+QzklttzS97v5C6cvjGK5if1zqFNEdskmUz6ggs7FQfPsK8DtY9HVWplAw==")
        PDBC_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/3dc8e15a453f4109928b82948e1cf1ce/execute?api-version=2.0&details=true")

        GSG_ML_KEY = os.environ.get("API_KEY", "wmqwEYBSE3IqPIlFAXqXHAx/Pa1nTDQnsL6/ZB4mlpv6X7YIIOE2PpUzrmePhqVIIitdYVbaT/oHhmegOjN//Q==")
        GSG_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/1e321f9a89834fdb84138589a28eda6e/execute?api-version=2.0&details=true")

        MORT_ML_KEY = os.environ.get("API_KEY", "XJg1jk5vbd59+u3uX+q0Nn+7u7kzA4FVN7QoTLaoiPyFz6EuGENXZjyejVRhjj5S5XPOyU1ARRKk0Gror0RNzQ==")
        MORT_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/1ab49df3ef7d4b34ac35e1125bd69566/execute?api-version=2.0&details=true")

        VNQ_ML_KEY = os.environ.get("API_KEY", "szJppS8Xj/SyzRgmg44tqeGxSOVzRhV/1gMG5TU3l0s9xEmfH+1ZZ6SelSDUgd4i8cITqjRwYuKNK9gG569GUA==")
        VNQ_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/1ebda07f5b83468fa934325b157c5759/services/9b0ca03dd5b94782854e6b2fc35db3b7/execute?api-version=2.0&details=true")

        # Construct the HTTP request header
        # HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}
        VFH_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ VFH_ML_KEY)}
        VGT_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ VGT_ML_KEY)}
        YLCO_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ YLCO_ML_KEY)}
        IHI_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ IHI_ML_KEY)}
        IEO_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ IEO_ML_KEY)}
        VDC_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ VDC_ML_KEY)}
        DBC_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ DBC_ML_KEY)}
        FREL_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FREL_ML_KEY)}
        AGG_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ AGG_ML_KEY)}

        IYF_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ IYF_ML_KEY)}
        KRE_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ KRE_ML_KEY)}
        FTEC_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FTEC_ML_KEY)}
        FDN_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FDN_ML_KEY)}
        RYU_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ RYU_ML_KEY)}
        FUTY_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FUTY_ML_KEY)}
        FHLC_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FHLC_ML_KEY)}
        XHE_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ XHE_ML_KEY)}
        XLE_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ XLE_ML_KEY)}
        PXI_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ PXI_ML_KEY)}
        FSTA_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ FSTA_ML_KEY)}
        IYK_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ IYK_ML_KEY)}
        PDBC_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ PDBC_ML_KEY)}
        GSG_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ GSG_ML_KEY)}
        MORT_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ MORT_ML_KEY)}
        VNQ_HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ VNQ_ML_KEY)}

# str.encode
        # Formulate the request
        #req = urllib.request.Request(URL, body, HEADERS)
        
        vfh_req = urllib.request.Request(VFH_URL, body_list[0], VFH_HEADERS)
        vgt_req = urllib.request.Request(VGT_URL, body_list[1], VGT_HEADERS)
        ylco_req = urllib.request.Request(YLCO_URL, body_list[2], YLCO_HEADERS)
        ihi_req = urllib.request.Request(IHI_URL, body_list[3], IHI_HEADERS)
        ieo_req = urllib.request.Request(IEO_URL, body_list[4], IEO_HEADERS)
        vdc_req = urllib.request.Request(VDC_URL, body_list[5], VDC_HEADERS)
        dbc_req = urllib.request.Request(DBC_URL, body_list[6], DBC_HEADERS)
        frel_req = urllib.request.Request(FREL_URL, body_list[7], FREL_HEADERS)
        agg_req = urllib.request.Request(AGG_URL, body_list[8], AGG_HEADERS)

        iyf_req = urllib.request.Request(IYF_URL, body_list[9], IYF_HEADERS)
        kre_req = urllib.request.Request(KRE_URL, body_list[10], KRE_HEADERS)
        ftec_req = urllib.request.Request(FTEC_URL, body_list[11], FTEC_HEADERS)
        fdn_req = urllib.request.Request(FDN_URL, body_list[12], FDN_HEADERS)
        ryu_req = urllib.request.Request(RYU_URL, body_list[13], RYU_HEADERS)
        futy_req = urllib.request.Request(FUTY_URL, body_list[14], FUTY_HEADERS)
        fhlc_req = urllib.request.Request(FHLC_URL, body_list[15], FHLC_HEADERS)
        xhe_req = urllib.request.Request(XHE_URL, body_list[16], XHE_HEADERS)
        xle_req = urllib.request.Request(XLE_URL, body_list[17], XLE_HEADERS)
        pxi_req = urllib.request.Request(PXI_URL, body_list[18], PXI_HEADERS)
        fsta_req = urllib.request.Request(FSTA_URL, body_list[19], FSTA_HEADERS)
        iyk_req = urllib.request.Request(IYK_URL, body_list[20], IYK_HEADERS)
        pdbc_req = urllib.request.Request(PDBC_URL, body_list[21], PDBC_HEADERS)
        gsg_req = urllib.request.Request(GSG_URL, body_list[22], GSG_HEADERS)
        mort_req = urllib.request.Request(MORT_URL, body_list[23], MORT_HEADERS)
        vnq_req = urllib.request.Request(VNQ_URL, body_list[24], VNQ_HEADERS)


        # Send this request to the AML service and render the results on page
        try:
            request_list =  [vfh_req, vgt_req, ylco_req, ihi_req, ieo_req, vdc_req, dbc_req, frel_req, agg_req,iyf_req,kre_req,ftec_req,fdn_req,ryu_req,futy_req,fhlc_req,xhe_req,xle_req,pxi_req,fsta_req,iyk_req,pdbc_req,gsg_req,mort_req,vnq_req]
            
            # response = requests.post(VFH_URL, headers=HEADERS, data=body)
            result_list = []
            a = 0
            for i in request_list: 
                response = urllib.request.urlopen(i)
                respdata = response.read()
                result = json.loads(str(respdata, 'utf-8'))
                result = do_something_pretty(result)
                result = json.dumps(result, indent=4, sort_keys=True)
                result_list.append([etf_tickers[a],result])
                a += 1

            for i in result_list:
                if i[0] == current_etf_global:
                    result = i[1]

            a = 0
            for i in weights_chosen:
                a += i 
                if a > 100: 
                    answer = "Your portfolio is overweighted (greater than 100). Please re-adjust on the previous pane."
                elif a < 100:
                    answer = "Your portfolio is does not add up to 100%. Please return to the previous pane and re-weight if you so wish."
                else: 
                    answer = "Congratulations! Your portfolio equates 100%, and your weights are the following:"

            if sum(weights_chosen[:1]) > 50: 
                risk_portfolio = "Low Risk and Safer Growth"
            elif sum(weights_chosen[:1]) > 25: 
                risk_portfolio = "Medium Risk and Higher Growth Potential"
            else: 
                risk_portfolio = "High Risk and Aggressive Growth/Loss Potential"

            return render_template (
                'final_result.html',
                title= 'The following prediction was made for the return of your portfolio:',
                result=result,
                etfg = current_etf_global,
                agg_result = result_list[8][1],
                energyt = tickers_chosen[0],
                techt = tickers_chosen[1],
                utilt = tickers_chosen[2],
                fint = tickers_chosen[3],
                healtht = tickers_chosen[4],
                constapt = tickers_chosen[5],
                condisct = tickers_chosen[6],
                answer = answer,
                risk_answer = risk_portfolio,
                etf_lbs = str(weights_chosen[0]) + str('%'),
                bonds_lbs = str(weights_chosen[1]) + str('%'),
                stock_lbs = str(sum(weights_chosen[2:])) + str('%'),
                close = closing_price
  
            )
    # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'final_result.html',
                title='There was an error',
             result=result
            )
            
        
        
    return render_template(
                'result.html',
                form=form,
                title="Your portfolio:",
                etf_content = longbusinesssum_G,
                etfg = current_etf_global,
                tyg = three_yr_G,
                fyg = five_yr_G,
                yrg = ytd_return_G,
                tyagg_g = three_yr_agg_G, 
                fyagg_g = five_yr_agg_G,
                yragg_g = ytd_return_agg_G,
             
                lbsagg_g = longbusinesssum_agg_G, 
                # thg = topholdings_G,

                # th_realestate = topholdings_G[0]['realestate']['fmt'],
                # th_consumer = topholdings_G[1]['consumer_cyclical']['fmt'],
                # th_basic = topholdings_G[2]['basic_materials']['fmt'],
                # th_consumerdef = topholdings_G[3]['consumer_defensive']['fmt'],
                # th_tech = topholdings_G[4]['technology']['fmt'],
                # th_communication = topholdings_G[5]['communication_services']['fmt'],
                # th_financial = topholdings_G[6]['financial_services']['fmt'],
                # th_utilities = topholdings_G[7]['utilities']['fmt'],
                # th_industrials = topholdings_G[8]['industrials']['fmt'],
                # th_energy = topholdings_G[9]['energy']['fmt'],
                # th_health = topholdings_G[10]['healthcare']['fmt'],
                # aaa_ratings = bondratings_bonds_G[2]['aaa']['fmt'],
                # aa_ratings = bondratings_bonds_G[1]['aa']['fmt'],
                # a_ratings = bondratings_bonds_G[3]['a']['fmt'],
                # bbb_ratings = bondratings_bonds_G[6]['bbb']['fmt'],


                #iframe = 'https://www.nasdaq.com/market-activity/stocks'

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
    output_bayesian=f'Our machine learning model predicted a closing value of {str(round(float(scored_label),2))} USD for the 30th trading day following {date.today()}.'
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output_bayesian
