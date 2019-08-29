import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            This model was created to take a look into the California HMRs and to test a base predictive model.
            However, this is from a relatively small data sample with limited features.To predict a value such
            as hospital mortality rates with a sufficient degree of accuracy would require a plethora of variables
            that were not provided in this dataset.

            Displayed on the right is feature importances from several features of the model. 

            """
        ),
    ],
    md=5,
)


column2 = dbc.Col(
    [
        
    ]
)

layout = dbc.Row([column1, column2])