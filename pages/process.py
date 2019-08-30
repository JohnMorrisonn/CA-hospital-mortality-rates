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
            ## Modeling Process - Takeaways
            --------------------------------------------------------------
                
            * ### Cleaning:  



            ![](assets/DF.PNG)

            This dataset is mortality rate information from the state of California. Being that it is clinical data, 
            it is often expected to be messy. Clinical data may be interpreted by a physician, recorded by a scribe, 
            and later documented at another date. Due to this, a condition may be misdiagnosed, may not have all of the information
            needed, or may have different abbreviations resulting in different values in a database. There is often
            human error, and this dataset fits right into this list.  

            &emsp;
     

            * ### Goal/Baseline:

            The goal is to predict the expected number of deaths for select procedures and conditions in these California hospitals.
            To prepare for the predictive model, the data was split based on the years. Train data was 2012-2013, validation data was 2014,
            and test data was 2015.

            A linear regression was used for the baseline model comparing the train data to the validation data with the `Mean Absolute Error`
            and `R^2 score` to beat below.

            `MAE: 3.408`

            `R^2: 0.472`  


            &emsp;

            * ### XGBoost Regressor:

            To improve the model's prediction accuracy, an gradient boosting model, `XGBoost Regressor`, was chosen due to the datas lack of 
            linear correlations and the `XGBoost Regressor`'s better known performance for intricate relationships. 

            After tuning and prepping the data with `RandomizedSearchCV`, `early_stopping_rounds`, and `OrdinalEncoder` the final model was tested
            on the validation data
            ```
            gb_pipeline = make_pipeline(
            ce.OrdinalEncoder(),
            XGBRegressor(n_estimators=250, learningrate=0.1, max_depth=4, objective='reg:squarederror', random_state=42, n_jobs=-1))

            gb_pipeline.fit(X_train, y_train)
            y_pred = gb_pipeline.predict(X_val)
            print('Gradient Boosting R^2:', r2_score(y_val, y_pred))
            ```
            `Gradient Boosting R^2`: __0.823__
            
            The score was heavily improved, and the dataset was chosen to fit the full train and validation data in order to finally predict the test data.
            ```
            train = newdf.query('Year <= 2014')
            X_train = train[features]
            y_train = train[target]

            gb_pipeline = make_pipeline(
                ce.OrdinalEncoder(),
                XGBRegressor(n_estimators=250, learningrate=0.1, max_depth=4, objective='reg:squarederror', random_state=42, n_jobs=-1)
                )

            gb_pipeline.fit(X_train, y_train)
            y_pred = gb_pipeline.predict(X_test)
            print('Gradient Boosting R^2:', r2_score(y_test, y_pred))
            ```
            `Gradient Boosting R^2`: __0.832__

            Further analysis of the predictions can be shown in the [Insights](https://california-hmr.herokuapp.com/insights) page.   

            &emsp;

            * ### Takeaways

            Cleaning and EDA is always mentioned as important, but when you get to confusing and messy data such as this you realize how important it becomes.
            This project has primarily shown me three key areas to focus on in the future.
            
            1. Always dig deeper into the features and data until you fully understand them. 
            Reading anything about where the data comes from, the data dictionary to the dataset, or further understanding the topic at hand will give you an advantage.
            
            2. Leaks will not always be obvious and may require digging to find out one feature you don't understand has been created based off the value of your target.

            3. Keeping the notebook organized as you work is a necessary step to be able to go back and make edits in your work. Even if you are slow with this process, it
            is still guaranteed to save time.
            





            """
            
        ),

    ],
)

layout = dbc.Row([column1])