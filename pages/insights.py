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
            ----------------------------------------------------------------------
            This model was created to take a look into the California HMRs and to test a base predictive model.
            However, this is from a relatively small data sample with limited features.To predict a value such
            as hospital mortality rates with a sufficient degree of accuracy would require a plethora of variables
            that were not provided in this dataset.

            Partial Dependency Plots of the top two features, Number of Cases and Hospital Ratings, and the least important
            feature, Year, are displayed to the right.

            The number of cases being extremely important gives note that a high number of patients are still heading 
            into the hospital for these conditions or procedures that have a higher probability of death.
            
            The hospital ratings high importance shows that they correlate with the number of deaths predicted giving
            more meaning to the initial ratings.
            
            Lastly, the year being of least importance shows that the time gap is too small between 2012-2015 to see a
            significant difference in the number of deaths for these conditions/procedures.

            Below are all of the features rated by importance in predicting the number of deaths, and a shaply plot
            showing a specific prediction with each feature's weighted value in the prediction.

            """
        ),
        html.Br(),
        html.Div(html.Img(src='assets/Feature Importance.PNG', className='img-fluid')),
        html.Br(),
        html.Div(html.Img(src='assets/shap.PNG', className='img-fluid'))
    ],
    md=7,
)


column2 = dbc.Col(
    [
        
        html.Div(html.Img(src='assets/PDP_Cases.PNG', className='img-fluid')),
        html.Br(),
        html.Div(html.Img(src='assets/PDP_ratings.PNG', className='img-fluid')),
        html.Br(),
        html.Div(html.Img(src='assets/PDP_year.PNG', className='img-fluid')),
    ]
)

layout = dbc.Row([column1, column2])