import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            #### Which Areas of Medical Care need Improvement?
                 
            To the right is an example graph of the Risk Adjusted Mortality Rates(RAMR) of hospitals in California from 2012-2015. These RAMRs 
            are currently used to rate hospitals and show which hospitals need improvement.

            Hospitals today have made extraordinary leaps in their practices, research, and technology geared towards the care of the patient.
            However, this is by no means a stopping point in the improvements of hospitals.

            In order to take the first step towards improving these outcomes, we must first understand and target the areas to prioritize
            these efforts.  

            This app uses data from [HealthData.gov](https://healthdata.gov/dataset/california-hospital-inpatient-mortality-rates-and-quality-ratings)
            to create a base model of predicting California hospital mortality rates (HMRs) based on several factors: medical procedure/condition, hospital ratings,
            number of cases per procedure/condition, and other factors provided by HealthData.gov. 


            """
        ),
        dcc.Link(dbc.Button('Base Predictive Model', color='primary'), href='/predictions')
    ],
    md=5,
)

# Cleaning Function
def wrangle(X):
    '''
    Drop the ID column and RAMR. RAMR is a leak in the prediction of Number_Deaths
    Remove all the STATE values that are sums of all the other columns
    Remove Procedures that change between the years
    Change the hospital ratings to reflect negative/postive weights
    '''
    X = X.copy()
    
    X = X.drop(columns=['OSHPDID'])
    
    # Change column names to more appropriate names without caps
    X = X.rename(columns={'YEAR':'Year', 'COUNTY':'County', 'HOSPITAL':'Hospital', 
                        'Risk Adjuested Mortality Rate':'RAMR',
                        'Procedure/Condition':'Procedure_Condition',
                        '# of Deaths':'Number_Deaths',
                        '# of Cases':'Number_Cases', 'Hospital Ratings':'Hospital_Ratings',
                        'LONGITUDE':'Longitude', 'LATITUDE':'Latitude'
                       })  
    
    # Remove rows where the value is for the entire state
    X = X.query("County != 'AAAA'") # AAAA is county code for State

    # Remove procedures_conditions that are not in every year, repetitive ones,
    # and hidden NaN values
    X.replace({'AAA Repair':np.nan, 'AAA Repair Unruptured':np.nan, 'Acute Stroke':np.nan, 
               'Pancreatic Other':np.nan, '.':np.nan}, inplace=True)
    X.dropna(inplace=True)
    
    # Change numeric columns from string to float
    numerics = ['Number_Deaths', 'Number_Cases']
    for column in numerics:
        X[column] = X[column].astype(float)
    
    # Creating numeric values for hospital rating since it is in least to best
    X['Hospital_Ratings'].replace({'Worse':-1, 'As Expected':0, 'Better':1}, inplace=True)
    
    return X


# Read in the dataframe
df = pd.read_csv('https://raw.githubusercontent.com/JohnMorrisonn/CA-hospital-mortality-rates/master/CA_Hosp_Mortality.csv', encoding = 'ISO-8859-1')
df = wrangle(df)

# Remove RAMR for leaks
newdf = df.drop(columns='RAMR')

# Graph the hospitals with Number_Deaths
fig = px.scatter(df, x="Year", y="RAMR", color="Hospital_Ratings")

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])