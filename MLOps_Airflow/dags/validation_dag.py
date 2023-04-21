import logging
import os
import pandas as pd
import pickle

from airflow import DAG
from airflow.models.dag import get_last_dagrun
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.db import provide_session
from csv import DictWriter
from datetime import datetime

from scripts.validation_script import validation


default_args = {
    'owner': 'Iago'
}

@provide_session
def _get_execution_date_of_dag_datasets(exec_date, session=None,  **kwargs):
    dag_datasets_last_run = get_last_dagrun(
        'dataset_creation', session)
    logging.info('Last dataset run: ', dag_datasets_last_run.execution_date)
    return dag_datasets_last_run.execution_date


def evaluate(models_path, val_path, results_path):
    """
    Given a path to models folder and a path to te validation dataset, add a row to results path for each model
    results.

    Parameters
    ----------
    models_path: path to directory where models to test are stored. (str)
    val_path: path to validation dataset. (str)
    results_path: path to historical validation dataset. (str)

    Returns
    -------
    A new row will be added to historical validation dataset for each model with its validation scores. The row will
    have the following columns:
    - model: model name. (str)
    - train_date: datetime when the last training was performed. (datetime)
    - val_date: datetime when the validation was performed. (datetime)
    - hyperparameters: values of the hyperparameters according to the model.
    - mae, wmape, rmse, tweedie: validation metrics. (float)
    """
    historic_df = pd.read_csv(results_path)
    last_train_date_df = historic_df.sort_values('train_date').groupby('model').tail(1)
    last_train_date = {}
    for index, row in last_train_date_df.iterrows():
        last_train_date[row['model']] = row['train_date']

    for model_file in os.listdir(models_path):
        with open(models_path + model_file, 'rb') as file:
            model = pickle.load(file)

        model_name = model_file.split('.')[0]
        results = validation(model, model_name, val_path)
        train_date = last_train_date[model_name]
        results['train_date'] = train_date
        results['train_requested'] = False
        logging.info(results)

        with open(results_path, 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=historic_df.columns)
            dictwriter_object.writerow(results)


with DAG(dag_id='test_models',
        description='DAG that will get trigger daily to validate the active models.',
        schedule='0 0 * * *',
        default_args=default_args,
        start_date=datetime(2023, 1, 1),
        catchup=False
) as dag:

    dataset_sensor = ExternalTaskSensor(
        task_id='eval_dataset_sensor',
        external_dag_id='dataset_creation',
        external_task_id=None,
        execution_date_fn=_get_execution_date_of_dag_datasets,
        mode='reschedule'
    )

    evaluate_task = PythonOperator(
        task_id='evaluate',
        python_callable=evaluate,
        op_kwargs={
            'models_path': './shared_volume/models/',
            'val_path': './shared_volume/data/test_data.csv',
            'results_path': './shared_volume/data/historical_validation.csv'
        }
    )

    dataset_sensor >> evaluate_task
