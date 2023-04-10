import csv
import logging
import pickle

from airflow import DAG
from airflow.models.dag import get_last_dagrun
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.db import provide_session
from datetime import datetime
from sklearn.linear_model import LinearRegression

from scripts.train_script import train
from scripts.validation_script import validation


@provide_session
def _get_execution_date_of_dag_datasets(exec_date, session=None,  **kwargs):
    dag_datasets_last_run = get_last_dagrun(
        'dataset_creation', session)
    logging.info('Last dataset run: ', dag_datasets_last_run.execution_date)
    return dag_datasets_last_run.execution_date


def train_model(eval_path, train_path, results_path, models_path):
    """
    This function performs the training and evaluation of the model. Once trained and evaluated, a new
    instance is written in the historical dataset, which will contain the model performance represented by different
    metrics, the date of the training and validation date, as well as the model name and its hyperparameters. Finally,
    the model is saved in a .sav file.

    Parameters
    ----------
    eval_path: path that indicates the validation dataset. (str)
    train_path: path that indicates the training dataset. (str)
    results_path: path that indicates the historical dataset where the new model instance is written. (str)
    models_path: path that indicates the folder where the models are saved. (str)

    Returns
    -------
    New instance generated in the historical dataset.
    New file of the trained model saved in the model directory. (.sav)
    """

    # In case we have different types of models, a condition is necessary
    model_name = 'linear_F_4'
    if model_name.split('_')[0] == 'linear':
        model = LinearRegression(fit_intercept=False, n_jobs=4)
    else:
        model = LinearRegression(fit_intercept=False, n_jobs=4)

    # We train the model with the correspondent hyperparameters
    trained_model, train_date = train(model, train_path)

    # We have to compute the performance with the evaluation script
    results = validation(trained_model, model_name, eval_path)

    # Write the row in the results_path csv
    with open(results_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['linear_F_4',  # Model name
                         results['val_date'],
                         train_date,
                         False,
                         4,
                         results['mae'],
                         results['wmape'],
                         results['rmse'],
                         results['tweedie'],
                         False])

    # Now we save the trained model with his correspondent name
    pickle.dump(model, open(models_path + 'linear_F_4' + '.sav', 'wb'))


default_args = {
    'owner': 'Iago'
}

dag = DAG(dag_id='linear_F_4',
          description='DAG that will get triggered monthly to train the correspondent model.',
          schedule='0 0 1 * *',
          default_args=default_args,
          start_date=datetime(2023, 2, 1),
          catchup=False)

with dag:
    dataset_sensor = ExternalTaskSensor(
        task_id='train_dataset_sensor',
        external_dag_id='dataset_creation',
        external_task_id=None,
        execution_date_fn=_get_execution_date_of_dag_datasets,
        mode='reschedule'
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        op_kwargs={
            'eval_path': './shared_volume/test_data.csv',
            'train_path': './shared_volume/train_data.csv',
            'results_path': './shared_volume/historical_validation.csv',
            'models_path': './shared_volume/models/'
        }
    )

    dataset_sensor >> train_task