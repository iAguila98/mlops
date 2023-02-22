import os
import pandas as pd
import plotly.express as px
import subprocess
import streamlit as st
import time


# Web configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto"
)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


# Main title of the page
logo_url = 'data:image/png;base64,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'
st.image(logo_url, width=250)
st.title('Monitoring Models trained on M5 Dataset')

# Description of the page functionality
st.write('Monitor different trained models on the M5 preprocessed dataset. Check different types of '
         'analysis and metrics.')

# Visualize historical graph validation
st.subheader('Historical Graph')
historical = pd.read_csv('MLOps_Airflow/shared_volume/historical_validation.csv')
models_path = 'MLOps_Airflow/shared_volume/models'
column_metrics = ['mae', 'wmape', 'rmse', 'tweedie']
tabs = st.tabs(['mae', 'wmape', 'rmse', 'tweedie'])


def plot_historical(dataset, metrics, graphs):
    """
    From the dataset of historical validations of the models, a graph is generated for each of the calculated metrics.
    The graph shows each trained model performance.

    Parameters
    ----------
    dataset: historical validation dataset. It stores the trained models performances over time.
    metrics: metrics computed in the validation.
    graphs: it corresponds to the metric tabs from streamlit. Each tab shows the graph that corresponds to the metric.

    Returns
    -------
    The plotted historical validation graphs for each metric.
    """
    for i, tab in enumerate(graphs):
        fig = px.line(dataset, x='val_date', y=metrics[i], color="model", markers=True)
        tab.plotly_chart(fig, use_container_width=True)


# Define two columns for the validate button and the refresh button
cols = st.columns(2)
# Button used to refresh the graphic with the new validations
with cols[0]:
    st.button("REFRESH", on_click=plot_historical(historical, column_metrics, tabs))

# Button used to manually trigger the validations of the trained models
with cols[1]:
    button = st.button('VALIDATE')

# Activates the validation button
if button:
    # Initialize while loop parameters
    initial_len = len(historical)
    len_csv = len(historical)
    model_num = len(os.listdir(models_path))

    # Make a manual trigger of the DAG that validates the models (through a shell script)
    subprocess.call('MLOps_Frontend/trigger_validation.sh')

    st.info('The evaluation process has been activated.', icon="ℹ️")

    # Wait until the DAG is done, specifically until a new row is added in the historical dataset
    while len_csv - initial_len != model_num:
        time.sleep(2)
        historical = pd.read_csv('MLOps_Airflow/shared_volume/historical_validation.csv')
        len_csv = len(historical)

    # Read the new instance created with the activation of the button
    st.subheader('New instance generated')
    st.table(historical.drop('train_requested', axis=1).tail(model_num))

    # Give an explanation to the users about the functionality of the buttons
    st.success('Click REFRESH to add this instance into the graph.', icon="✅")
    st.info('If you click VALIDATE again, the last instance will be automatically added to the graph.', icon="ℹ️")


