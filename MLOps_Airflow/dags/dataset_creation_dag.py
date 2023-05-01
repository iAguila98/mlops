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


def add_data(data_path, data_batch_path, events_dict_path, snaps_dict_path):
    """
    Generates new rows and adds them to the data, which is saved in a .csv file. In addition, it saves this new batch
    of data in another file so that you can later create more data from it, avoiding reading the entire data.

    Parameters
    ----------
    data_path: Path where the data file is saved. (str)
    data_batch_path: Path where the new data batch is saved. (str)
    events_dict_path: Path where the events of a year are saved. (str)
    snaps_dict_path: Path where the snaps of a year are saved. (str)

    Returns
    -------
    Updates the original data and the new batch of data.
    """
    # Generate new batch of data and save it to use it as base for the next batch
    new_batch_data = generate_data(data_batch_path, events_dict_path, snaps_dict_path)
    new_batch_data.to_csv(data_batch_path, index=False)

    # Add new batch to the original csv dataset
    with open(data_batch_path, 'r') as f1:
        next(f1)
        batch = f1.read()

    with open(data_path, 'a') as f2:
        f2.write(batch)


def preprocess_split_data(data_path, pre_data_path, train_path, test_path):
    """
    Preprocess the updated data, taking into account the old data, which is required to perform some of the
    preprocessing techniques. After preprocessing, the dataset is split into train and test sets. For the test set the
    last calendar year of the data is selected and for the train set the remaining data is selected.

    Parameters
    ----------
    data_path: Path where the data file is saved. (str)
    pre_data_path: Path where the preprocessed data file is saved. (str)
    train_path: Path where the train data file is saved. (str)
    test_path: Path where the test data file is saved. (str)

    Returns
    -------
    New preprocessed data and train-test sets.
    """
    # Preprocess the data taking into account the new batch
    new_data = pd.read_csv(data_path)
    preprocessed_data = preprocessing_pipeline(new_data)
    preprocessed_data.to_csv(pre_data_path)

    # Get last year that indicates the train-test split
    last_day = new_data['date'].iat[-1]
    last_day = datetime.strptime(last_day, "%Y-%m-%d")
    last_year = datetime.strftime(datetime(last_day.year - 1, last_day.month, last_day.day), "%Y-%m-%d")

    # Prepare and save train and test dataset
    train_data = preprocessed_data[preprocessed_data['date'] < last_year]
    train_set = train_data.set_index('date')
    train_set.to_csv(train_path)

    # Prepare and save train and test dataset
    test_data = preprocessed_data[preprocessed_data['date'] >= last_year]
    test_set = test_data.set_index('date')
    test_set.to_csv(test_path)


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
            'data_path': './shared_volume/data/extracted.csv',
            'data_batch_path': './shared_volume/data/batch_data.csv',
            'events_dict_path': './shared_volume/data/events_dictionary.pkl',
            'snaps_dict_path': './shared_volume/data/snaps_dictionary.pkl'
        }
    )

    preprocess_split_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_split_data,
        op_kwargs={
            'data_path': './shared_volume/data/extracted.csv',
            'pre_data_path': './shared_volume/data/preprocessed_data.csv',
            'train_path': './shared_volume/data/train_data.csv',
            'test_path': './shared_volume/data/test_data.csv'
        }
    )

    add_data_task >> preprocess_split_data_task