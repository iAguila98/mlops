import json
import logging
import os
import time

import pandas as pd
import subprocess

from file_creation import create_dag

logging.basicConfig(level=logging.INFO)

# Reading the historical validation dataset
historical_path = 'MLOps_Airflow/shared_volume/data/historical_validation.csv'
data = pd.read_csv(historical_path)
filtered_data = data[data['train_requested']==True]

# We have to delete the train_requested=TRUE row after reading it.
base_df = data[data['train_requested']!=True].set_index('model')
base_df.to_csv(historical_path)

# Setting the parameters of the create_dag function
dag_id = filtered_data.iloc[0]['model']

# Target path
new_filename = 'MLOps_Airflow/dags/' + dag_id + '.py'

# Check if the DAG file does not exist in order to be created
if not os.path.exists(new_filename):
    logging.info('Model not detected, creating a new model...')

    # Reading the hyperparameters of the model
    hyperparameters = []
    initial_hyperparameter = 3  # First hyperparameter is column index = 3 in the historical dataset
    last_hyperparameter = data.shape[1]-5  # Last 5 columns corresponds to performance and train_requested columns
    for i in range(initial_hyperparameter, last_hyperparameter):
        hyperparameters.append(filtered_data.iloc[0][i])

    # We create the dag (this will be executed automatically the webserver detects it)
    create_dag(new_filename, dag_id, hyperparameters)

    # Create an empty json where we will save the dag information
    df = pd.DataFrame()
    df.to_json('MLOps_Airflow/shared_volume/dag_info.json')

    # Wait until dag_id can be read. When this happens, it means that the DAG exists
    num_retries = 150
    sleep_time = 2
    dag_error = None
    for x in range(0, num_retries):  # Try 150 times, aprox. 5 minutes of waiting
        try:
            dag_error = None
            # Execute shell scripts that gets the basic information of the DAG
            file_ = open('MLOps_Airflow/shared_volume/dag_info.json', 'w')
            p = subprocess.Popen(['MLOps_Airflow/shared_volume/check_dag_exists.sh', dag_id], stdout=file_)
            p.wait()  # Waits until the subprocess is finished

            # Check the status of the DAG. If it is 404 it means that it is still not created
            f = open('MLOps_Airflow/shared_volume/dag_info.json')
            data = json.load(f)
            status = data['dag_id']

        # When the DAG does not exist, we can't read the 'dag_id' key so the loop continues
        except Exception as e:
            dag_error = str(e)

        if dag_error:
            time.sleep(sleep_time)
        # When the DAG exists, the status variable will save the 'dag_id' from the json and the loop will end
        else:
            os.remove('MLOps_Airflow/shared_volume/dag_info.json')
            break

    # Execute the following code only when the number of attempts has not been exceeded
    if not dag_error:
        # Create an empty json where we will save the run information
        df = pd.DataFrame()
        df.to_json('MLOps_Airflow/shared_volume/dag_run_info.json')

        # Now we can trigger the DAG manually and save the dag run information
        file_ = open('MLOps_Airflow/shared_volume/dag_run_info.json', 'w')
        subprocess.Popen(['MLOps_Airflow/shared_volume/trigger_train.sh', dag_id], stdout=file_)
    else:
        # Send a message to be aware of the error
        logging.error('Number of attempts exceeded.')
        # We need to delete the file to start a new experiment
        os.remove('MLOps_Airflow/shared_volume/dag_info.json')

# If the DAG already exists we just trigger it and save the dag run information
else:
    logging.info('Model detected, triggering the retraining...')

    # Create an empty json where we will save the run information
    df = pd.DataFrame()
    df.to_json('MLOps_Airflow/shared_volume/dag_run_info.json')

    # Now we can trigger the DAG manually and save the dag run information
    file_ = open('MLOps_Airflow/shared_volume/dag_run_info.json', 'w')
    subprocess.Popen(['MLOps_Airflow/shared_volume/trigger_train.sh', dag_id], stdout=file_)

