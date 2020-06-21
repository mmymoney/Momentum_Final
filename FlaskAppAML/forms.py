from wtforms import Form, StringField, TextAreaField, validators, RadioField
# from flask import Flask, render_template
# from flask_wtf import Form
# from wtforms.fields import DateField
# from flask_bootstrap import Bootstrap
from datetime import datetime

class SubmissionForm(Form):
    # Date = DateField(id='datepick',default="2020-05-27")
    Age = RadioField('Title', coerce=int, choices=[('5','Less than 45'),('4','45 to 55'),('3','56 to 65'), ('2','66 to 75'), ('1','75 or older')])
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