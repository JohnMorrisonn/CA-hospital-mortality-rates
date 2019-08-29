import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import shap
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from dash.dependencies import Input, Output
from joblib import load
from app import app


##-----------------------------------------------------------------------------------------

## Dataframe cleaning function

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

##-----------------------------------------------------------------------------------------

## Load in the data and perform the pipeline to create predicted values

# Read in the dataframe
df = pd.read_csv('https://raw.githubusercontent.com/JohnMorrisonn/CA-hospital-mortality-rates/master/CA_Hosp_Mortality.csv', encoding = 'ISO-8859-1')
df = wrangle(df)

# Remove RAMR for leaks, but keep in df for future purposes
newdf = df.drop(columns='RAMR')

target = 'Number_Deaths'
features = newdf.columns.drop('Number_Deaths').tolist()

train = newdf.query('Year <= 2014')
test = newdf.query('Year == 2015')

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

pipeline = load('assets/gb_pipeline (1).joblib')
y_pred = pipeline.predict(X_test)

X_test['Predicted'] = y_pred


##-----------------------------------------------------------------------------------------

## Plots and Graphs

# Shap Plot
# row = X_test.iloc[[1200]]

# explainer = shap.TreeExplainer(gb)
# row_encoded = encoder.transform(row)
# shap_values = explainer.shap_values(row_encoded)

# shap.initjs()
# shap.force_plot(
#     base_value=explainer.expected_value,
#     shap_values=shap_values,
#     features=row
# )


##-----------------------------------------------------------------------------------------


## Front-end Dash app



column1 = dbc.Col(
    [
        dcc.Markdown(
            """   
            ### Base Predictive Model

            Select the specific county and procedure or condition to compare the predicted result to the actual number of deaths.

            """
        ),
        

        html.Br(),

    # County dropdown selection    
        dcc.Markdown('#### County'),
        dcc.Dropdown(
            id='County',
            options=[
                {'label': 'Alameda', 'value': 'Alameda'},
                {'label': 'Amador', 'value': 'Amador'},
                {'label': 'Butte', 'value': 'Butte'},
                {'label': 'Calaveras', 'value': 'Calaveras'},
                {'label': 'Colusa', 'value': 'Colusa'},
                {'label': 'Contra Costa', 'value': 'Contra Costa'},
                {'label': 'Del Norte', 'value': 'Del Norte'},
                {'label': 'El Dorado', 'value': 'El Dorado'},
                {'label': 'Fresno', 'value': 'Fresno'},
                {'label': 'Glenn', 'value': 'Glenn'},
                {'label': 'Humboldt', 'value': 'Humboldt'},
                {'label': 'Imperial', 'value': 'Imperial'},
                {'label': 'Inyo', 'value': 'Inyo'},
                {'label': 'Kern', 'value': 'Kern'},
                {'label': 'Kings', 'value': 'Kings'},
                {'label': 'Lake', 'value': 'Lake'},
                {'label': 'Lassen', 'value': 'Lassen'},
                {'label': 'Los Angeles', 'value': 'Los Angeles'},
                {'label': 'Madera', 'value': 'Madera'},
                {'label': 'Marin', 'value': 'Marin'},
                {'label': 'Mariposa', 'value': 'Mariposa'},
                {'label': 'Mendocino', 'value': 'Mendocino'},
                {'label': 'Merced', 'value': 'Merced'},
                {'label': 'Modoc', 'value': 'Modoc'},
                {'label': 'Mono', 'value': 'Mono'},

            ],
            value='Alameda'
        ),

        html.Br(),

    # Procedure/Condition dropdown selection    
        dcc.Markdown('#### Procedure/Condition'),
        dcc.Dropdown(
            id='PC',
            options=[
                {'label': 'AMI', 'value': 'AMI'},
                {'label': 'Acute Stroke Hemorrhagic', 'value': 'Acute Stroke Hemorrhagic'},
                {'label': 'Acute Stroke Ischemic', 'value': 'Acute Stroke Ischemic'},
                {'label': 'Acute Stroke Subarachnoid', 'value': 'Acute Stroke Subarachnoid'},
                {'label': 'Carotid Endarterectomy', 'value': 'Carotid Endarterectomy'},
                {'label': 'Craniotomy', 'value': 'Craniotomy'},
                {'label': 'Esophageal Resection', 'value': 'Espophageal Resection'},
                {'label': 'GI Hemorrhage', 'value': 'GI Hemorrhage'},
                {'label': 'Heart Failure', 'value': 'Heart Failure'},
                {'label': 'Hip Fracture', 'value': 'Hip Fracture'},
                {'label': 'PCI', 'value': 'PCI'},
                {'label': 'Pancreatic Cancer', 'value': 'Pancreatic Cancer'},
                {'label': 'Pancreatic Resection', 'value': 'Pancreatic Resection'},
                {'label': 'Pneumonia', 'value': 'Pneumonia'}
            ],
            value='AMI'
        )      
    ],
    md=4,
)



column2 = dbc.Col(
    [
        dcc.Graph(
            id='prediction-graph', 
            figure={
                'data': [
                    {
                        'x': X_test['County'],
                        'y': y_test,
                        'mode': 'bar',
                    }
                ]
            },
            style={'width': '80%',
                'margin-left': 'auto',
                'margin-right': 'auto'
            }),
    ]
)

layout = dbc.Row([column1, column2])


## Callbacks

@app.callback(
    Output('prediction-graph', 'figure'),
    [Input(component_id='County', component_property='value'),
    Input(component_id='PC', component_property='value')]
)
def graph(County, PC):

    mask = (X_test['County'] == County) & (X_test['Procedure_Condition'] == PC)
    
    layout= go.Layout(
        yaxis={'title': 'Number of Deaths'},
        barmode='group'
    )

    data=[
        go.Bar(name='Actual', x=X_test[mask]['County'], y=y_test),
        go.Bar(name='Predicted', x=X_test[mask]['County'], y=y_pred)
    ]

    return {'data':data, 'layout':layout}


