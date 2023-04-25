import json
import logging
import os
import time
import yaml

import pandas as pd
import subprocess

from file_creation import create_dag

logging.basicConfig(level=logging.INFO)

# Read paths from the YAML
with open('MLOps_Airflow/shared_volume/config.yaml') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)
    data_paths = config['data_paths']
    scripts_paths = config['scripts_paths']
    coms_paths = config['coms_paths']

# Reading the historical validation dataset
data = pd.read_csv(data_paths['historical_path'])
filtered_data = data[data['train_requested']==True]

# We have to delete the train_requested=TRUE row after reading it.
base_df = data[data['train_requested']!=True].set_index('model')
base_df.to_csv(data_paths['historical_path'])

# Setting the parameters of the create_dag function
dag_id = filtered_data.iloc[0]['model']

# Target path
dag_path = 'MLOps_Airflow/dags/' + dag_id + '.py'
model_path = 'MLOps_Airflow/shared_volume/models/' + dag_id + '.sav'

# If the DAG file and the model does not exist, create the new DAG
if not os.path.exists(dag_path) and not os.path.exists(model_path):
    logging.info('DAG and model not detected, creating a new model DAG...')

    # Reading the hyperparameters of the model
    hyperparameters = []
    initial_hyperparameter = 3  # First hyperparameter is column index = 3 in the historical dataset
    last_hyperparameter = data.shape[1]-5  # Last 5 columns corresponds to performance and train_requested columns
    for i in range(initial_hyperparameter, last_hyperparameter):
        hyperparameters.append(filtered_data.iloc[0][i])

    # We create the dag (this will be executed automatically the webserver detects it)
    create_dag(dag_path, dag_id, hyperparameters)

    # Create an empty json where we will save the dag information
    df = pd.DataFrame()
    df.to_json(coms_paths['train_dag_info_path'])

    # Wait until dag_id can be read. When this happens, it means that the DAG exists
    num_retries = 150
    sleep_time = 2
    dag_error = None
    for x in range(0, num_retries):  # Try 150 times, aprox. 5 minutes of waiting
        try:
            dag_error = None
            # Execute shell scripts that gets the basic information of the DAG
            file_ = open(coms_paths['train_dag_info_path'], 'w')
            p = subprocess.Popen([coms_paths['check_dag_exists'], dag_id], stdout=file_)
            p.wait()  # Waits until the subprocess is finished

            # Check the status of the DAG. If it is 404 it means that it is still not created
            f = open(coms_paths['train_dag_info_path'])
            data = json.load(f)
            status = data['dag_id']

        # When the DAG does not exist, we can't read the 'dag_id' key so the loop continues
        except Exception as e:
            dag_error = e

        if dag_error:
            time.sleep(sleep_time)
        # When the DAG exists, the status variable will save the 'dag_id' from the json and the loop will end
        else:
            os.remove(coms_paths['train_dag_info_path'])
            break

    # Create an empty json where we will save the run information
    df = pd.DataFrame()
    df.to_json(coms_paths['train_run_info_path'])

    # Now we can trigger the DAG manually and save the dag run information
    file_ = open(coms_paths['train_run_info_path'], 'w')
    p = subprocess.Popen([coms_paths['trigger_train_path'], dag_id], stdout=file_)
    p.wait()  # Waits until the subprocess is finished

    if dag_error:
        # Send a message to be aware of the problem
        logging.info('Number of attempts exceeded.')
        # We need to delete the file to start a new try
        os.remove(coms_paths['train_dag_info_path'])

# If the DAG already exists, trigger it and save the dag run information
elif os.path.exists(dag_path):
    logging.info('DAG detected, trying to trigger the training...')

    # Create an empty json where we will save the run information
    df = pd.DataFrame()
    df.to_json(coms_paths['train_run_info_path'])

    # Now we can trigger the DAG manually and save the dag run information
    file_ = open(coms_paths['train_run_info_path'], 'w')
    p = subprocess.Popen([coms_paths['trigger_train_path'], dag_id], stdout=file_)
    p.wait()  # Waits until the subprocess is finished

# Raise an exception when the situation is not expected to happen
else:
    raise Exception('DAG model no longer exists.')
