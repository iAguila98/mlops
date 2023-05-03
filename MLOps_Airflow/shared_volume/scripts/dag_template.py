import csv
import logging
import numpy as np
import pickle

from airflow import DAG
from airflow.models.dag import get_last_dagrun
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.db import provide_session
from datetime import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from scripts.train_script import train
from scripts.evaluation_script import evaluation


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


def train_model(eval_path, train_path, results_path, models_path):
    """
    This function performs the training and evaluation of the model. Once trained and evaluated, a new
    instance is written in the historical dataset, which will contain the model performance represented by different
    metrics, the date of the training and evaluation date, as well as the model name and its hyperparameters. Finally,
    the model is saved in a .sav file.

    Parameters
    ----------
    eval_path: Path that indicates the test dataset. (str)
    train_path: path that indicates the training dataset. (str)
    results_path: path that indicates the historical dataset where the new model instance is written. (str)
    models_path: path that indicates the folder where the models are saved. (str)

    Returns
    -------
    New instance generated in the historical dataset.
    New file of the trained model saved in the model directory. (.sav)
    """
    # Define the model according to the model type selected by the user
    model_name = dag_id_model
    model_type = model_name.split('_')[0]

    # Initialize the possible string values related to the max_features hyperparameter
    auto = 'auto'
    sqrt = 'sqrt'
    log2 = 'log2'

    # For the linear regression model
    if model_type == 'linear':
        model = LinearRegression(fit_intercept=fit_intercept_model, n_jobs=n_jobs_model)

    # For the decision tree regressor model
    elif model_type == 'decision':
        model = DecisionTreeRegressor(max_depth=d_max_depth_model, max_leaf_nodes=max_leaf_nodes_model,
                                      max_features=d_max_features_model)

    # For the gradient boosting regressor model
    elif model_type == 'gradient':
        model = GradientBoostingRegressor(learning_rate=learning_rate_model, n_estimators=n_estimators_model,
                                          max_depth=g_max_depth_model, max_features=g_max_features_model)

    # There are no more type models implemented
    else:
        raise Exception('Model name not implemented.')

    # We train the model with the correspondent hyperparameters
    trained_model, train_date = train(model, train_path)

    # We have to compute the performance with the evaluation script
    results = evaluation(trained_model, model_name, eval_path)

    # Save the row that has to be written in historical dataset
    row = [model_name,
           results['eval_date'],
           train_date,
           fit_intercept_model,
           n_jobs_model,
           d_max_depth_model,
           max_leaf_nodes_model,
           d_max_features_model,
           learning_rate_model,
           n_estimators_model,
           g_max_depth_model,
           g_max_features_model,
           results['mae'],
           results['wmape'],
           results['rmse'],
           results['tweedie'],
           False]

    # Adapt possible None values to strings in order to write them in the historical_dataset.csv
    for idx, el in enumerate(row):
        if el is None:
            el = 'None'
            row[idx] = el

    # Write the row in the results_path csv
    with open(results_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    # Now we save the trained model with his correspondent name
    pickle.dump(model, open(models_path + model_name + '.sav', 'wb'))


default_args = {
    'owner': 'Iago'
}

dag = DAG(dag_id=dag_id_model,
          description='DAG that will get triggered weekly to train the correspondent model.',
          schedule='0 0 * * 0',
          default_args=default_args,
          start_date=start_date_change,
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
            'eval_path': './shared_volume/data/test_data.csv',
            'train_path': './shared_volume/data/train_data.csv',
            'results_path': './shared_volume/data/historical_dataset.csv',
            'models_path': './shared_volume/models/'
        }
    )

    dataset_sensor >> train_task
