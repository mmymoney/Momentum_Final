   import requests 

   # get-analysis
   # get-detail
   # get-statistics
   # get-historical-data
  
   #ETF: fiveyearaverage, threeyearaverage,keystatics-ytdReturn, 
   url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
    querystring = {"symbol":current_etf}
    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
     print(response.text)

    #ETF: topholdings-sectorweightings, assetprofile-longBusinessSummary
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"

    querystring = {"region":"US","lang":"en","symbol":"spy"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #Bonds: yield(fmt)
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"

    querystring = {"region":"US","symbol":"agg"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #Bonds: topholdings-bondRatings(all), longBusinessSummary
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"

    querystring = {"region":"US","lang":"en","symbol":"agg"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #STOCKS: longBusinessSummary, 
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"

    querystring = {"region":"US","lang":"en","symbol":"spy"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #STOCK: fiftytwoweekhigh, fiftytwoweeklow,
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"

    querystring = {"region":"US","symbol":"aapl"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #STOCK: closingprice

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

    querystring = {"frequency":"1d","filter":"history","period1":"1546448400","period2":"1562086800","symbol":"aapl"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    #STOCK: recommendation trend(currentperiod), financialdata-returnonequity
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"

    querystring = {"symbol":"aapl"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)