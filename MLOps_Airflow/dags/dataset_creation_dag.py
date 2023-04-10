import pandas as pd

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    'owner': 'Iago',
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}


def get_test_df(data_path, val_path):
    """
    Given a data_path to a warehouse dataset (located in a shared volume), a test dataset is created with
    the last year data at the test_path.

    Parameters
    ----------
    data_path: path to warehouse dataset. (str)
    val_path: path to store validation_dataset. (str)

    Returns
    -------
    Validation dataset with the last year data created at val_path. (.csv)
    """
    column_to_skip = ['Unnamed: 0']
    df = pd.read_csv(data_path, usecols=lambda x: x not in column_to_skip)
    df['date'] = pd.to_datetime(df['date'])
    today = pd.to_datetime('now', utc=True).date() - pd.Timedelta(10*365, 'day')  # Now it's set to 10 years earlier as
    today_last_year = today - pd.Timedelta(365, 'day')                            # our dataset data stops at 2018
    test_df = df.set_index('date')[today_last_year:today]
    test_df.to_csv(val_path)
    del df


def get_train_df(data_path, train_path):
    """
    From the preprocessed dataset, the training dataset that will be used by the models to be trained is generated.
    This training dataset is defined with a time range, namely those instances that are between 10 years ago and 7 years
    ago with respect to the current year. It has to be taken into account that the dataset records instances between
    2011 and 2016.

    Parameters
    ----------
    data_path: path to warehouse dataset (preprocessed dataset)
    train_path: path where the training dataset is saved after selecting the training instances.

    Returns
    -------

    """
    column_to_skip = ['Unnamed: 0']
    df = pd.read_csv(data_path, usecols=lambda x: x not in column_to_skip)
    df['date'] = pd.to_datetime(df['date'])
    seven_years_ago = pd.to_datetime('now', utc=True).date() - pd.Timedelta(7 * 365, 'day')  # 7 years earlier
    ten_years_ago = seven_years_ago - pd.Timedelta(3 * 365, 'day')  # 10 years ago
    train_df = df.set_index('date')[ten_years_ago:seven_years_ago]
    train_df.to_csv(train_path)
    del df


with DAG(
        dag_id='dataset_creation',
        description='DAG that will get trigger daily to create train and evaluate datasets.',
        schedule='0 0 * * *',
        default_args=default_args,
        start_date=datetime(2023, 1, 1),
        catchup=False
) as dag:

    eval_dataset_task = PythonOperator(
        task_id='eval_dataset',
        python_callable=get_test_df,
        op_kwargs={
            'data_path': './shared_volume/preprocessed_data.csv',
            'val_path': './shared_volume/test_data.csv'
        }
    )

    train_dataset_task = PythonOperator(
        task_id='train_dataset',
        python_callable=get_train_df,
        op_kwargs={
            'data_path': './shared_volume/preprocessed_data.csv',
            'train_path': './shared_volume/train_data.csv'
        }
    )

    eval_dataset_task >> train_dataset_task

# sensor = ExternalTaskSensor(task_id='dag_sensor', external_dag_id = 'another_dag_id', external_task_id = None, dag=dag, mode = 'reschedule')
#
# task = DummyOperator(task_id='some_task', retries=1, dag=dag)
#
# task.set_upstream(sensor)