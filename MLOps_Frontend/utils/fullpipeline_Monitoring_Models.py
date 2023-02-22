import pickle
import pandas as pd
import plotly.express as px
import streamlit as st

from csv import writer
from datetime import datetime

from MLOps_Frontend.utils import custom_web

# Web configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto"
)

# Load pickle models
with open('MLOps_Airflow/shared_volume/models/linear_T_1.sav', 'rb') as li:
    lin_reg = pickle.load(li)


@st.cache
def load_data():
    # Read dataset and perform the splitting
    dataset = pd.read_csv('MLOps_Airflow/shared_volume/preprocessed_data.csv', index_col=0)
    # Split the dataset
    _, _, val_data, val_label, test_data, test_label = custom_web.splitting(dataset)

    return val_data, val_label, test_data, test_label

# Load split dataset
val_X, val_y, test_X, test_y = load_data()

# Main title of the page
logo_url = 'data:image/png;base64,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'
st.image(logo_url, width=250)
st.title('Monitoring Models trained on M5 Dataset')

# Description of the page functionality
st.write('Monitor different trained models on the M5 preprocessed dataset. Check different types of '
         'analysis and metrics.')

with st.sidebar:
    # Sidebar title
    logo_url_2 = 'data:image/jpeg;base64,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'
    st.image(logo_url_2, width=200)
    st.header('Manual Validation')

    # Model selection
    models = ['Linear Regression']
    model = st.selectbox('Select the model to validate:', models)

    # Button for extra visualization
    extra = st.checkbox('Show options for extra visualization:')

    # If the user checks extra visualization
    if extra:
        # Select analysis type
        analysis = ['Sales', 'Categories', 'States']
        analysis_option = st.selectbox('Select the type of analysis:', analysis)


        # In the case of 'sales' analysis, the threshold that distinguishes between big sale or low sale is selected.
        if analysis_option == 'Sales':
            thresh_sales = st.slider('What do you consider to be a big number of sales?:', 1, 100)

        # Metric selection to be computed
        metrics = ['MAE', 'WMAPE', 'RMSE', 'Tweedie']
        selected_metrics = st.multiselect('Select the metrics:', metrics)

    # Validation model button
    button = st.button('VALIDATE')

# Visualize historical graph validation
st.subheader('Historical Graph')
historical = pd.read_csv('MLOps_Airflow/shared_volume/historical_validation.csv')
column_metrics = ['mae', 'wmape', 'rmse', 'tweedie']
tabs = st.tabs(['mae', 'wmape', 'rmse', 'tweedie'])

for i,tab in enumerate(tabs):
    fig = px.line(historical, x='date', y=column_metrics[i], color="model", markers=True)
    tab.plotly_chart(fig, use_container_width=True)

# Activates the validation button
if button:
    # For now, we only have one trained model, so it will always be the linear model.
    if model == 'Linear Regression':
        trained_model = lin_reg
    else:
        trained_model = lin_reg

    # Compute the different metrics with all the validation data
    mae, wmape, rmse, tweedie = custom_web.reg_global_analysis(model=trained_model,
                                                               val_X=val_X, val_y=val_y)

    # Add a new row to the csv (historical validation dataset)
    new_row = [model, datetime.now(), mae, wmape, rmse, tweedie]
    with open('MLOps_Frontend/historical_validation.csv', 'a') as f_object:
        writer(f_object).writerow(new_row)
        f_object.close()

    # Read the new instance created with the activation of the button
    st.subheader('New instance generated')
    st.write(historical.tail(1))

    # The extra visualization button is checked
    if extra:
        st.subheader('Extra Validation Information')

        # Execute if the 'Sales' analysis is selected
        if analysis_option == 'Sales':

            # Call an external function to compute the metrics regarding the analysis type
            mae, wmape, rmse, tweedie = custom_web.reg_sales_analysis(model=trained_model,
                                                                      big_sales=thresh_sales,
                                                                      val_X=val_X, val_y=val_y)

            # Call an external function to show the results regarding the analysis type
            custom_web.show_sales_analysis(selected_metrics=selected_metrics,
                                           mae=mae, wmape=wmape, rmse=rmse, tweedie=tweedie)

        # Execute if the 'Categories' analysis is selected
        elif analysis_option == 'Categories':

            # Call an external function to compute the metrics regarding the analysis type
            mae, wmape, rmse, tweedie = custom_web.reg_categories_analysis(model=trained_model,
                                                                           val_X=val_X, val_y=val_y)

            # Call an external function to show the results regarding the analysis type
            custom_web.show_categories_analysis(selected_metrics=selected_metrics,
                                                mae=mae, wmape=wmape, rmse=rmse, tweedie=tweedie)

        # Execute if the 'States' analysis is selected
        elif analysis_option == 'States':

            # Call an external function to compute the metrics regarding the analysis type
            mae, wmape, rmse, tweedie = custom_web.reg_states_analysis(model=trained_model,
                                                                       val_X=val_X, val_y=val_y)

            # Call an external function to show the results regarding the analysis type
            custom_web.show_states_analysis(selected_metrics=selected_metrics,
                                            mae=mae, wmape=wmape, rmse=rmse, tweedie=tweedie)