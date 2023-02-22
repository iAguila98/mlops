import json
import os
import time

import pandas as pd
import subprocess
import streamlit as st

from csv import DictWriter

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


logo_url = 'data:image/png;base64,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'
st.image(logo_url, width=250)
st.title('Train models')

st.write('View best performing models and train new ones selecting model type and hyper parameters.')
historical_path = 'MLOps_Airflow/shared_volume/historical_validation.csv'


def load_data(path):
    return pd.read_csv(path)


def get_last_model_row(df):
    rows_df = df.sort_values('train_date').groupby('model').tail(1)
    rows_df = rows_df.loc[:, df.columns != 'train_requested']
    rows_df.rename(columns={'model': 'Model name', 'val_date': 'Validation date', 'train_date': 'Training date'},
                   inplace=True)
    return rows_df


h_dataset = load_data(historical_path)
last_models_rows = get_last_model_row(h_dataset)

st.table(last_models_rows)  #, use_container_width=True)
model_types = ['Select Model Type', 'Linear regression', 'Decision tree', 'Random forest']

model_type = st.selectbox('Model type', model_types)

if model_type == 'Linear regression':
    col1, col2 = st.columns(2)
    with col1:
        fit_intercept = st.selectbox('Fit Intercept', [True, False])

    with col2:
        n_jobs = st.selectbox('Number of jobs used', [-1, 1, 2, 3, 4])

    model_name = "_".join(['linear', str(fit_intercept)[0], str(n_jobs)])
    training_dict = {'model': model_name,
                     'fit_intercept': fit_intercept,
                     'n_jobs': n_jobs,
                     'train_requested': True}

    # Save the model path
    model_path = 'MLOps_Airflow/shared_volume/models/' + model_name + '.sav'

    if 'dag_run_id' not in st.session_state:
        st.session_state.dag_run_id = ''
    if 'run_ready' not in st.session_state:
        st.session_state.run_ready = False

    if st.button('Launch Training'):

        with open(historical_path, 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=h_dataset.columns)
            dictwriter_object.writerow(training_dict)

        # Execute the dag_generation code to create the dag file
        cmd = ['python', 'MLOps_Airflow/shared_volume/dag_generation.py']
        subprocess.Popen(cmd)

        # Wait until it detects a DAG run and save the dag_run_id to check its status
        while True:
            try:
                # Read the dag_run_id in the json file
                f = open('MLOps_Airflow/shared_volume/dag_run_info.json')
                data = json.load(f)
                st.session_state.dag_run_id = data['dag_run_id']
            except:
                continue
            else:
                os.remove('MLOps_Airflow/shared_volume/dag_run_info.json')
                break

        st.session_state.run_ready = True

        st.success('The trigger has been executed. Click Refresh to check the run status.', icon="✅")
        st.warning('WARNING: If you click LAUNCH TRAINING again, the button will trigger another training execution.'
                   ,icon = "⚠️")


    # Initialize refresh button
    refresh_button = st.button('Check Run Status')

    # Refresh button to check the run status after the trigger execution (training button)
    if refresh_button == True and st.session_state.run_ready == True:

        # Initialize arguments used in the request to REST API
        dag_id = model_name
        dag_run_id = st.session_state.dag_run_id

        # Execute the request which returns the info about the DAG run and save it
        file_ = open('MLOps_Frontend/run_status.json', 'w')
        subprocess.Popen(['MLOps_Frontend/check_status.sh', dag_id, dag_run_id], stdout=file_ )
        time.sleep(2) # Give some time to make the request and obtain the DAG run info

        # Read the status from the DAG run info extracted
        f = open('MLOps_Frontend/run_status.json')
        data = json.load(f)
        state = data['state']

        # Conditions to show messages to the user depending on the DAG run status
        if state == 'success':
            st.success('The training is completed.', icon="✅")
        elif state == 'failed':
            st.error('The training has failed.', icon="🚨")
        elif state == 'running':
            st.info('The process is running.', icon="ℹ️")
        else:
            st.warning('Status not expected. Please check the status in the Airflow Webserver: http://localhost:8080/'
                       , icon="ℹ️")

    # If the launch training process has not finished yet, display the following message
    if refresh_button == True and st.session_state.run_ready == False:
        st.info('The trigger has not been processed yet, please try again in a few minutes.', icon="ℹ️")


elif model_type == 'Select Model Type':
    pass

else:
    st.write('Still working on it...')
