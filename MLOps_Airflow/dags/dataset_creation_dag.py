import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.add_data_script import generate_data
from scripts.preprocessing import preprocessing_pipeline

default_args = {
    'owner': 'Iago',
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}


def add_data(data_path, data_batch_path):
    """

    Parameters
    ----------
    data_path
    data_batch_path

    Returns
    -------

    """
    # Generate new batch of data and save it to use it as base for the next batch
    new_batch_data = generate_data(data_batch_path)
    new_batch_data.to_csv(data_batch_path, index=False, header=False)

    # Add new batch to the original csv dataset
    with open(data_batch_path, 'r') as f1:
        batch = f1.read()

    with open(data_path, 'a') as f2:
        f2.write(batch)


def preprocess_data(data_path, pre_data_path, train_path):
    """

    Parameters
    ----------
    data_path
    pre_data_path
    train_path

    Returns
    -------

    """
    # Preprocess the data taking into account the new batch
    new_data = pd.read_csv(data_path)
    preprocessed_data = preprocessing_pipeline(new_data)
    preprocessed_data.to_csv(pre_data_path)

    # Prepare and save train dataset
    train_set = preprocessed_data[preprocessed_data['date'] >= '2014-01-30']
    train_set.to_csv(train_path)


with DAG(
        dag_id='dataset_creation',
        description='DAG that will get trigger daily to add new data, preprocess it and get the train set.',
        schedule='0 0 * * *',
        default_args=default_args,
        start_date=datetime(2023, 1, 1),
        catchup=False
) as dag:

    add_data_task = PythonOperator(
        task_id='add_data',
        python_callable=add_data,
        op_kwargs={
            'data_path': './shared_volume/extracted.csv',
            'data_batch_path': './shared_volume/batch_data.csv'
        }
    )

    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        op_kwargs={
            'data_path': './shared_volume/extracted.csv',
            'pre_data_path': './shared_volume/preprocessed_data.csv',
            'train_path': './shared_volume/train_data.csv'
        }
    )

    add_data_task >> preprocess_data_task