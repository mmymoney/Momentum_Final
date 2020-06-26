# import requests 
# import json

# #ETF: fiveYrAvgReturnPct, threeyearaverage,keystatics-ytdReturn, 
# #ETF: topholdings-sectorweightings, assetprofile-longBusinessSummary
# #BONDS: ALSO APPLICABLE
# url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"

# querystring = {"region":"US","lang":"en","symbol":current_etf}

# headers = {
#     'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
#     'x-rapidapi-key': "ca07005c56mshafe5b7a7c516a9dp1b90e2jsn1e7c85e6edd1"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)
# response_json_etf2 = response.json()
# three_yr = response_json_etf2['defaultKeyStatistics']['threeYearAverageReturn']['fmt']
# five_yr = response_json_etf2['defaultKeyStatistics']['fiveYearAverageReturn']['fmt']
# ytd_return = response_json_etf2['defaultKeyStatistics']['ytdReturn']['fmt']
# topholdings = response_json_etf2['topHoldings']['sectorWeightings']
# longbusinesssum = response_json_etf2['assetProfile']['longBusinessSummary']
# bondratings_bonds = response_json_etf2['topHoldings']['bondRatings']
# longbusinesssum_stocks = response_json_etf2['summaryProfile']['longBusinessSummary']
# fiftytwoweekhigh_stocks = response_json_etf2['summaryDetail']['fiftyTwoWeekHigh']['fmt']
# fiftytwoweeklow_stocks = response_json_etf2['summaryDetail']['fiftyTwoWeekLow']['fmt']
# prevs_close_stocks = response_json_etf2['summaryDetail']['previousClose']['fmt']
# recomm_trend_stocks = response_json_etf2['recommendationTrend']['trend'][0]
# ROE_stocks = response_json_etf2['financialData']['returnOnEquity']['fmt']

    
#     longbusinesssum_stocks = response_json_etf2['summaryProfile']['longBusinessSummary']
#     fiftytwoweekhigh_stocks = response_json_etf2['summaryDetail']['fiftyTwoWeekHigh']['fmt']
#     fiftytwoweeklow_stocks = response_json_etf2['summaryDetail']['fiftyTwoWeekLow']['fmt']
#     prevs_close_stocks = response_json_etf2['summaryDetail']['previousClose']['fmt']
#     recomm_trend_stocks = response_json_etf2['recommendationTrend']['trend'][0]
#     ROE_stocks = response_json_etf2['financialData']['returnOnEquity']['fmt']