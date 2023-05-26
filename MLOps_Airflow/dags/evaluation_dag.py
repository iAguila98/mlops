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

from scripts.evaluation_script import evaluation


default_args = {
    'owner': 'Iago'
}


@provide_session
def _get_execution_date_of_dag_datasets(*args, session=None, **kwargs):
    """
    The execution date of the last run from a specific DAG is obtained. It is used to build an ExternalTaskSensor
    which consists of waiting until a specific DAG has completed its execution before executing a different DAG.
    The @provide_session allows the function to feed parameters at runtime.

    Parameters
    ----------
    args: Required parameter to properly create the function to be called in the ExternalTaskSensor.
    session: Session provided by @provide_session.
    kwargs: Required parameter to properly create the function to be called in the ExternalTaskSensor.

    Returns
    -------
    The date of the last execution correspondent to the desired DAG (task to which it has to wait).
    """
    # Get the last run from the dataset_creation DAG
    dag_datasets_last_run = get_last_dagrun('dataset_creation', session=session)

    return dag_datasets_last_run.execution_date


def evaluate(models_path, eval_path, results_path):
    """
    Given a path to models folder and a path to te validation dataset, add a row to results path for each model
    results.

    Parameters
    ----------
    models_path: Path to directory where models to test are stored. (str)
    eval_path: Path to test dataset. (str)
    results_path: Path to historical dataset. (str)

    Returns
    -------
    A new row will be added to historical dataset for each model with its evaluation scores. The row will
    have the following columns:
    - model: Model name. (str)
    - train_date: Datetime when the last training was performed. (datetime)
    - eval_date: Datetime when the evaluation was performed. (datetime)
    - hyperparameters: Values of the hyperparameters according to the model.
    - mae, wmape, rmse, tweedie: Evaluation metrics. (float)
    """
    # From the historical_dataset.csv, get the date of the last training of each model
    historic_df = pd.read_csv(results_path)
    last_train_date_df = historic_df.sort_values('train_date').groupby('model').tail(1)
    last_train_date = {}
    for index, row in last_train_date_df.iterrows():
        last_train_date[row['model']] = row['train_date']

    # Read each model that has been previously created and trained
    for model_file in os.listdir(models_path):
        with open(models_path + model_file, 'rb') as file:
            model = pickle.load(file)

        # Evaluate the model and get the correspondent results
        model_name = model_file.split('.')[0]
        results = evaluation(model=model, model_name=model_name, eval_path=eval_path)

        # Get additional column values to write historical_dataset.csv
        train_date = last_train_date[model_name]
        results['train_date'] = train_date
        results['train_requested'] = False

        # Write the results in the historical_dataset.csv
        with open(results_path, 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=historic_df.columns)
            dictwriter_object.writerow(results)


with DAG(dag_id='test_models',
         description='DAG that will get trigger daily to evaluate the active models.',
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
            'eval_path': './shared_volume/data/test_data.csv',
            'results_path': './shared_volume/data/historical_dataset.csv'
        }
    )

    dataset_sensor >> evaluate_task
