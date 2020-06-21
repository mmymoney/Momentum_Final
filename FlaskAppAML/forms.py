from wtforms import Form, StringField, TextAreaField, validators, RadioField, SelectMultipleField
# from flask import Flask, render_template
# from flask_wtf import Form
# from wtforms.fields import DateField
# from flask_bootstrap import Bootstrap
from datetime import datetime

class SubmissionForm(Form):
    # Date = DateField(id='datepick',default="2020-05-27")
    email = StringField('Title', [validators.Length(min=0, max=100)],default = 'email@gmail.com')
    Age = RadioField('Title', coerce=int, choices=[('5','Less than 45'),('4','45 to 55'),('3','56 to 65'), ('2','66 to 75'), ('1','75 or older')])
    income_level = RadioField('Title', coerce=int, choices=[('5','$0 to $40,000'),('4','$40,001 to $65,000'),('3','$65,001 to $85,000'), ('2','$85,001 to $100,000'), ('1','$100,001 or more')])
    sector_preference = RadioField('Title', coerce=int, choices=[('5','Healthcare'),('4','Financial'),('3','Tech'), ('2','Consumer'), ('1','Communications')])
    citizenship = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes'),('2','Decline to answer')])
    education = RadioField('Title', coerce=int, choices=[('5','High School Diploma'),('4','Bachelors Degree'),('3','Post-Bac'), ('2','Masters'), ('1','Doctorate')])
    experience_years = RadioField('Title', coerce=int, choices=[('5','0 to 1 years'),('4','1 to 3 years'),('3','3 to 5 years'), ('2','5 to 10 years'), ('1','More than 10 years')])
    periodicals = SelectMultipleField('Title', coerce=int, choices=[('5','Wall Street Journal'),('4','MarketWatch'),('3','Economist'), ('2','SeekingAlpha'), ('1','Financial Times')])
    # experience_years = RadioField('Title', coerce=int, choices=[('5','0 to 1 years'),('4','1 to 3 years'),('3','3 to 5 years'), ('2','5 to 10 years'), ('1','More than 10 years')])
    aspirations = SelectMultipleField('Title', coerce=int, choices=[('5','Hobby / Recreation'),('4','Income source'),('3','Career'), ('2','Retirement'), ('1','Education / Research')])
    brokerage_acct = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes')])
    interested_in_learning = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes')])
    fin_info = StringField('Title', [validators.Length(min=0, max=100)],default = 'Your Financial Source')

    #Technical Assessment 
    hertz_scenario = RadioField('Title', coerce=int, choices=[('0','Being a holder of the companys stock, or equity holder'),('1','Be a holder of the companys debt, or debt holder')])
    put_option = RadioField('Title', coerce=int, choices=[('0','Rise'),('1','Fall')])
    safest_asset = RadioField('Title', coerce=int, choices=[('0','Gold'),('1','British Pound'),('2','Real Estate'),('3','Ethereum')])
    bonds = RadioField('Title', coerce=int, choices=[('0','Rise'),('1','Fall')])
    diversification = RadioField('Title', coerce=int, choices=[('0','No'),('1','Yes')])
    

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