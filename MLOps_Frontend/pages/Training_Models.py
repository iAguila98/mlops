import json
import os
import time
import yaml

import pandas as pd
import subprocess
import streamlit as st

from csv import DictWriter


@st.cache_resource
def read_config_yaml(yaml_path):
    """

    Parameters
    ----------
    yaml_path

    Returns
    -------

    """
    with open(yaml_path) as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        data_paths = config['data_paths']
        scripts_paths = config['scripts_paths']
        coms_paths = config['coms_paths']

    return data_paths, scripts_paths, coms_paths


def get_models_table(h_data):
    """

    Parameters
    ----------
    h_data

    Returns
    -------

    """
    rows_df = h_data.sort_values('train_date').groupby('model').tail(1)
    rows_df = rows_df.loc[:, h_data.columns != 'train_requested']
    rows_df.rename(columns={'model': 'Model name', 'val_date': 'Validation date', 'train_date': 'Training date'},
                   inplace=True)
    st.table(rows_df)


########################################################################################################################

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

# Insert logo and title
logo_url = "data:image/png;base64,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"
st.image(logo_url, width=500)
st.title('Training Models')

# Add a brief description of the page
st.write('On this page, you can see in the trained model table, all the types of models that have been trained. '
         'Specifically, it provides information about the last model trained for each of them. In addition, '
         'in this page it is possible to train already existing models or to create new ones by means of a model type '
         'and hyperparameters selection system.')


########################################################################################################################

# Read paths from the YAML
data_paths, scripts_paths, coms_paths = read_config_yaml('MLOps_Airflow/shared_volume/config.yaml')

# Show a table with the last registration of each model type
st.subheader('Trained Models Table')
historical = pd.read_csv(data_paths['historical_path'])
get_models_table(historical)

# Define model types selectbox in the dashboard
st.subheader('Train Your Model')
model_types = ['Linear Regression', 'Decision Tree', 'Gradient Boosting']
model_type = st.selectbox('Model type', model_types)

# Define possible hyperparameters and values for a linear regression model
if model_type == 'Linear Regression':

    # Define the hyperparameters and its values with selectbox
    col1, col2 = st.columns(2)
    with col1:
        fit_intercept = st.selectbox('Fit intercept', [True, False])

    with col2:
        n_jobs = st.selectbox('Number of jobs used', [-1, 1, 2, 3, 4])

    # Save required information to posteriorly start the training
    model_name = "_".join(['linear', str(fit_intercept)[0], str(n_jobs)])
    training_dict = {'model': model_name,
                     'fit_intercept': fit_intercept,
                     'n_jobs': n_jobs,
                     'train_requested': True}

# Define possible hyperparameters and values for a decision tree model
elif model_type == 'Decision Tree':

    # Define the hyperparameters and its values with selectbox
    col1, col2, col3 = st.columns(3)
    with col1:
        d_max_depth = st.selectbox('Max depth', [1, 3, 5, 7, 9])
    with col2:
        max_leaf_nodes = st.selectbox('Max leaf nodes', ['None', 20, 40, 60, 80])
    with col3:
        d_max_features = st.selectbox('Max features', ['None', 'auto', 'sqrt', 'log2'])

    # For max_leaf_nodes we will include the entire number in the model name, but only 'N' for None
    if max_leaf_nodes == 'None':
        aux = max_leaf_nodes[0]
    else:
        aux = str(max_leaf_nodes)

    # Save required information to posteriorly start the training
    model_name = "_".join(['decision', str(d_max_depth), aux, str(d_max_features)[0]])
    training_dict = {'model': model_name,
                     'd_max_depth': d_max_depth,
                     'max_leaf_nodes': max_leaf_nodes,
                     'd_max_features': d_max_features,
                     'train_requested': True}

# Define possible hyperparameters and values for a gradient boosting model
elif model_type == 'Gradient Boosting':

    # Define the hyperparameters and its values with selectbox
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        learning_rate = st.selectbox('learning_rate', [0.0001, 0.001, 0.01, 0.1, 1])
    with col2:
        n_estimators = st.selectbox('n_estimators', [1, 10, 50, 100, 200])
    with col3:
        g_max_depth = st.selectbox('g_max_depth', [1, 3, 5, 7, 9])
    with col4:
        g_max_features = st.selectbox('g_max_features', ['None', 'auto', 'sqrt', 'log2'])

    # Save required information to posteriorly start the training
    model_name = "_".join(['gradient', str(learning_rate).replace('.', ''), str(n_estimators), str(g_max_depth),
                           str(g_max_features)[0]])
    training_dict = {'model': model_name,
                     'learning_rate': learning_rate,
                     'n_estimators': n_estimators,
                     'g_max_depth': g_max_depth,
                     'g_max_features': g_max_features,
                     'train_requested': True}

# There are no more type models implemented
else:
    raise Exception('Model name not implemented.')


########################################################################################################################

# Save the model and dag path
model_path = 'MLOps_Airflow/shared_volume/models/' + model_name + '.sav'
dag_path = 'MLOps_Airflow/dags/' + model_name + '.py'

# Initialize dug_run_id argument used to check the dag run status
if 'train_run_id' not in st.session_state:
    st.session_state.train_run_id = ''

# Initialize the state variable used to define the while loop that checks the training run status
state = ''

# Define two columns for the training button and the refresh button
cols = st.columns(5)
with cols[0]:
    refresh_button = st.button('REFRESH')
with cols[1]:
    pass
with cols[2]:
    train_button = st.button('TRAIN')
with cols[3]:
    pass
with cols[4]:
    pass

# Define the 'launch training' button and what it should execute
if train_button:
    # Initialize second try variable, useful to inform the user properly
    second_try = False

    # Inform the user when the model already exists, and it is going to be retrained
    if os.path.exists(dag_path) and os.path.exists(model_path):
        st.info('The model and the DAG already exists. It is going to be retrained.', icon="ℹ️")

    # Inform the user when the model and its dag does not exist, and the dag has to be generated
    elif not os.path.exists(dag_path) and not os.path.exists(model_path):
        st.info('The model DAG does not exist. New orchestrated task is going to be generated. Airflow can take a few '
                'minutes to detect a new DAG.', icon="ℹ️")

    # Inform the user that Airflow is still waiting for the new dag, so it has to try again in a few minutes
    elif os.path.exists(dag_path) and not os.path.exists(model_path):
        st.info('New generated DAG exists, but there is no trained model. Airflow may still be awaiting detection.'
                , icon="ℹ️")
        second_try = True

    # Raise an exception when the situation is not expected to happen
    else:
        raise Exception('DAG model no longer exists.')

    # Write an initial row in the historical_validation dataset
    with open(data_paths['historical_path'], 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=historical.columns)
        dictwriter_object.writerow(training_dict)

    # Execute the dag_generation code to create the dag file
    cmd = ['python', scripts_paths['dag_generation_path']]
    p = subprocess.Popen(cmd)
    p.wait()  # Waits until the subprocess is finished

    # Make sure that there is time to detect new json files created in dag_generation.py
    time.sleep(2)

    # Try to read the dag_run_id from the json
    try:
        # Read and save the dag_run_id in the json file
        f = open(coms_paths['train_run_info_path'])
        data = json.load(f)
        st.session_state.train_run_id = data['dag_run_id']
        # Delete the json that contains the dag run id, used to check the status of the run
        os.remove(coms_paths['train_run_info_path'])

        # Ghost DAG can be executed successfully, therefore there is no problem and json can be deleted
        if os.path.exists(coms_paths['error_path']):
            os.remove(coms_paths['error_path'])

    # If dag_run_id or the json does not exist, there is an error
    except:

        # When there is a json that indicates the type of error
        if os.path.exists(coms_paths['error_path']):

            # Read the type of error that indicates
            f = open(coms_paths['error_path'])
            type_error = json.load(f)

            # When the error has been caused by reaching the maximum number of attempts to wait for DAG detection
            if type_error['error'] == 'max_attempts':

                # When the user has tried for the first time to train a new model but there is an error
                if second_try is False:
                    # Inform the user about the error
                    st.warning('Airflow is taking too long to detect the new model. The detection is still in '
                               'progress, but the training has been cancelled. Please, try ordering the training later.'
                               , icon="⚠️")

                # When the user has tried again to train the new model, but there is still an error
                else:
                    st.warning('Airflow has not yet detected the new dag. Please try again in a few minutes.'
                               , icon="⚠️")

                # We need to delete the train run and error files to start a new try
                os.remove(coms_paths['train_run_info_path'])
                os.remove(coms_paths['error_path'])

            # When the error has been caused by an incompletely deleted DAG
            else:
                st.warning('DAG existed previously but Airflow did not eliminate it completely. It has been reordered '
                           'for generation, but you will need to order the model training when this is completed.'
                           , icon="⚠️")

                # We need to delete the error file to start a new try
                os.remove(coms_paths['error_path'])

            # Stop the streamlit page execution
            st.stop()

        # When there isn't a json that indicates the type of error, we don't know its cause.
        else:
            # We need to delete the train run files to start a new try
            os.remove(coms_paths['train_run_info_path'])

            # Send a message to be aware of the problem
            raise Exception('Unknown error.')

    # St.empty() allows to overwrite messages that are shown to the user in streamlit
    with st.empty():

        # Inform that the trigger has been successfully ordered
        st.info('The training has been successfully ordered.', icon="ℹ️")
        time.sleep(3)  # Give time to the user to read the message

        # As long as the process has not been completed, whether successfully or not, keep in the loop.
        while state != 'success' and state != 'failed':

            # Initialize arguments used in the request to REST API
            dag_id = model_name
            dag_run_id = st.session_state.train_run_id

            # Execute the request which returns the info about the DAG run and save it
            file_ = open(coms_paths['train_run_status_path'], 'w')
            p = subprocess.Popen([coms_paths['check_train_run_status_path'],
                                  dag_id, dag_run_id], stdout=file_)
            p.wait()  # Waits until the subprocess is finished

            # Read the status from the DAG run info extracted
            f = open(coms_paths['train_run_status_path'])
            data = json.load(f)
            state = data['state']

            # Conditions to show messages to the user depending on the DAG run status
            if state == 'success':
                st.success('The training is completed.', icon="✅")
            elif state == 'failed':
                st.error('The training has failed.', icon="🚨")
            elif state == 'running':
                st.info('The training is being performed.', icon="ℹ️")
            elif state == 'queued':
                st.info('The training is in queue.', icon="ℹ️")
            else:
                st.info('Status not expected. Please check the status in the Airflow Webserver: '
                        'http://localhost:8080/', icon="ℹ️")

            # Wait 2 seconds before repeating the iteration again
            time.sleep(2)

        # Delete the run_status.json when the training is finished
        os.remove(coms_paths['train_run_status_path'])

# Refresh streamlit page
if refresh_button:
    st.empty()

