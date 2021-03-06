from wtforms import Form, StringField, TextAreaField, validators, RadioField, SelectMultipleField, FloatField, SelectField
# from flask import Flask, render_template
# from flask_wtf import Form
# from wtforms.fields import DateField
# from flask_bootstrap import Bootstrap
from datetime import datetime

class SubmissionForm(Form):
    # Date = DateField(id='datepick',default="2020-05-27")
    email = StringField('Title', [validators.Length(min=0, max=100)],default = '*youremail@gmail.com*')
    income_level = RadioField('Title', coerce=int, choices=[('5','$0 to $40,000'),('4','$40,001 to $65,000'),('3','$65,001 to $85,000'), ('2','$85,001 to $100,000'), ('1','$100,001 or more')])
    #dont think we need numbering for the ones that arent factored into the risk sensing - JS
    sector_preference = RadioField('Title', choices=[('Financial Sector', 'Financial Sector'),('Technology Sector', 'Technology Sector'),('Utilities', 'Utilities'), ('Healthcare', 'Healthcare'), ('Energy', 'Energy'),('Consumer Staples', 'Consumer Staples'),('Commodities', 'Commodities'),('Real Estate', 'Real Estate')])
    #sector_preference = RadioField('Title', coerce=int, choices=[('5','Healthcare'),('4','Financial'),('3','Tech'), ('2','Consumer'), ('1','Communications')])
    citizenship = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes'),('2','Decline to answer')])
    education = RadioField('Title', coerce=int, choices=[('5','High School Diploma'),('4','Bachelors Degree'),('3','Post-Bac'), ('2','Masters'), ('1','Doctorate')])
    experience_years = RadioField('Title', coerce=int, choices=[('5','0 to 1 years'),('4','1 to 3 years'),('3','3 to 5 years'), ('2','5 to 10 years'), ('1','More than 10 years')])
    periodicals = SelectMultipleField('Title', choices=[('Wall Street Journal','Wall Street Journal'),('MarketWatch','MarketWatch'),('Economist','Economist'), ('SeekingAlpha','SeekingAlpha'), ('Financial Times','Financial Times')], default = "No Response")
    aspirations = SelectMultipleField('Title', choices=[('Hobby / Recreation','Hobby / Recreation'),('Income Source','Income source'),('Career','Career'), ('Retirement','Retirement'), ('Education / Research','Education / Research')], default = "No Response")
    diversification = RadioField('Title', coerce=int, choices=[('5','No'),('1','Yes')])
    brokerage_acct = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes')])
    interested_in_learning = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes')])
    scenario_1 = RadioField('Title', coerce=int, choices=[('1','debt holder'),('5','equity holder')])
    #bond_interest = RadioField('Title', coerce=int, choices=[('1','lower'),('5','higher')])
    scenario_2 = RadioField('Title', coerce=int, choices=[('1','fall'),('5','rise')])
    port_diversified = RadioField('Title', coerce=int, choices=[('1','no'),('5','yes')])
    safest_asset = RadioField('Title', coerce=int, choices=[('1','real estate'),('5','ethereum'), ('2','gold'),('3','british pound')])
    income_drawing = RadioField('Title', coerce=int, choices=[('1','Not for at-least 20 years'),('2','10 to 20 years'),('3','5 to 10 years'), ('4','Not now, but within 5 years'), ('5','Immediately')])
    fin_info = StringField('Title', [validators.Length(min=0, max=100)],default = '*Enter Source*')
    return_expectations = RadioField('Title', coerce=int, choices=[('1','Aggressive growth'),('2','Significant growth'),('3','Moderate growth'), ('4','Mild growth'), ('5','Break-even')])
    normal_expectations = RadioField('Title', coerce=int, choices=[('1','Outperform the stock market'),('2','Track to the stock market'),('3','Slightly trail the stock market'), ('4','Grow moderately'), ('5','Grow with caution')])
    poor_expectations = RadioField('Title', coerce=int, choices=[('1','To make losses'),('2','To make very little or break even'),('3','To make out a little gain, i.e. 2-5%'), ('4','To make a modest gain'), ('5','To be affected little by the broader stock market movements')])
    three_yr_attitude = RadioField('Title', coerce=int, choices=[('1','I can tolerate a large loss'),('2','I can tolerate a moderate loss'),('3','I can tolerate a small loss'), ('4','It would be hard dealing with a loss'), ('5','I need to see at least a little return')])
    three_month_attitude = RadioField('Title', coerce=int, choices=[('1','I would not worry about losses in that time frame'),('2','A loss of more than 10% would concern me'),('3','I can only tolerate small short-term losses'), ('4','I would have a hard time stomaching any losses'), ('5','I would not be able to tolerate any losses')])
    age = RadioField('Title', coerce=int, choices=[('1','Less than 45'),('2','45 to 55'),('3','56 to 65'), ('4','66 to 75'), ('5','75 or older')])
    # weightings and tickers
    etf_weighting = FloatField("Title",default = 100)
    bond_weighting = FloatField("Title", default = 0)
    energy_weighting = FloatField("Title", default = 0)
    tech_weighting = FloatField("Title", default = 0)
    util_weighting = FloatField("Title", default = 0)
    fin_weighting = FloatField("Title", default = 0)
    health_weighting = FloatField("Title", default = 0)
    constap_weighting = FloatField("Title", default = 0)
    condisc_weighting = FloatField("Title", default = 0)

    energy_tickers = ['CVX','XOM','EOG']
    tech_tickers = ['MSFT','AAPL','V','MA','PYPL']
    util_tickers = ['NEE','D','DUK']
    fin_tickers = ['JPM','BAC','AXP']
    healthcare_tickers = ['JNJ','UNH','MRK','PFE','ABBV']
    constap_tickers = ['PG','PEP','KO','WMT']
    condisc_tickers = ['AMZN','HD','MCD','NKE','SBUX','TGT']

    energy_ticker = SelectField('Title', choices = energy_tickers)
    tech_ticker = SelectField('Title', choices = tech_tickers)
    util_ticker = SelectField('Title', choices = util_tickers)
    fin_ticker = SelectField('Title', choices = fin_tickers)
    health_ticker = SelectField('Title', choices = healthcare_tickers)
    constap_ticker = SelectField('Title', choices = constap_tickers)
    condisc_ticker = SelectField('Title', choices = condisc_tickers)

    

    # Open = StringField('Title', [validators.Length(min=0, max=30)],default = 287.75)
    # High = StringField('Title', [validators.Length(min=0, max=30)], default = 289.779999)
    # Low = StringField('Title', [validators.Length(min=0, max=30)],default = 287.130005)
    # Close = StringField('Title', [validators.Length(min=0, max=30)], default = 287.679993)
    # Volume = StringField('Title', [validators.Length(min=0, max=30)], default = 75250400)
    # T3_Vol_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = 5622800)
    # T3_Close_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = -4.109986)
    # T3_Open_Diff = StringField('Title',  [validators.Length(min=0, max=30)], default = -7.01001)
    # T2_Vol_Diff = StringField('Title',  [validators.Length(min=0, max=30)], default = 4319500)
    # T2_Close_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = -1.489991)
    # T2_Open_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = -1.109985)
    # T1_Vol_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = -1617800)
    # T1_Close_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = -3.429993)
    # T1_Open_Diff = StringField('Title', [validators.Length(min=0, max=30)], default = 0.290009)
    # Prior_Day_Vert_Delta_Ratio = StringField('Title', [validators.Length(min=0, max=30)], default = 0.566239)
    # Retracement_Signal = StringField('Title', [validators.Length(min=0, max=30)], default = 0.20754311)
    # Prior_Day_Derivative = StringField('Title', [validators.Length(min=0, max=30)], default = -0.0184704)