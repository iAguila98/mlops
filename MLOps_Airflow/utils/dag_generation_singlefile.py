import csv
import pickle
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sklearn.linear_model import LinearRegression

from scripts.train_script import train
from scripts.evaluate import reg_test


def create_dag(dag_id, schedule, default_args, hyperparameters):
    """

    Parameters
    ----------
    dag_id
    schedule
    default_args
    hyperparameters

    Returns
    -------

    """
    def get_train_df(data_path, train_path):
        """

        Parameters
        ----------
        data_path
        train_path

        Returns
        -------

        """
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        seven_years_ago = pd.to_datetime('now', utc=True).date() - pd.Timedelta(7 * 365, 'day')  # 7 years earlier
        ten_years_ago = seven_years_ago - pd.Timedelta(3 * 365, 'day')  # 10 years ago
        train_df = df.set_index('date')[ten_years_ago:seven_years_ago].drop('Unnamed: 0', axis='columns')
        train_df.to_csv(train_path)


    def train_model(eval_path, train_path, results_path, models_path):
        """

        Parameters
        ----------
        eval_path
        train_path
        results_path
        models_path

        Returns
        -------

        """

        # In case we have different types of models, a condition is necessary
        if dag_id.split('_')[0] == 'linear':
            model = LinearRegression(fit_intercept=hyperparameters[0], n_jobs=hyperparameters[1])
        else:
            model = LinearRegression(fit_intercept=hyperparameters[0], n_jobs=hyperparameters[1])

        # We train the model with the correspondent hyperparameters
        trained_model, train_date = train(model, train_path)

        # We have to compute the performance with the evaluation script
        results = reg_test(trained_model, eval_path)

        # Write the row in the results_path csv
        with open(results_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([dag_id,  # Model name
                             results['date'],
                             train_date,
                             hyperparameters[0],
                             hyperparameters[1],
                             results['mae'],
                             results['wmape'],
                             results['rmse'],
                             results['tweedie'],
                             False])

        # Now we save the trained model with his correspondent name
        pickle.dump(model, open(models_path + dag_id + '.sav', 'wb'))

    dag = DAG(dag_id=dag_id,
              description='DAG that will get triggered monthly to train the correspondent model.',
              schedule=schedule,
              default_args=default_args,
              start_date = datetime(2023, 1, 1),
              catchup = False)

    with dag:
        dataset_task = PythonOperator(
            task_id='train_dataset',
            python_callable=get_train_df,
            op_kwargs={
                'data_path': './shared_volume/old_preprocessed_data.csv',
                'train_path': './shared_volume/train_data.csv'
            }
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

        dataset_task >> train_task

    return dag


# Reading the historical validation dataset
data = pd.read_csv('./shared_volume/historical_validation.csv')
#data = pd.read_csv('/home/iagoaguila/Projects/MLOps_Project/mlops/MLOps_Airflow/shared_volume/historical_validation.csv')
filtered_data = data[data['train_requested']==True]

# Setting the parameters of the create_dag function
dag_id = filtered_data.iloc[0]['model']
schedule = '@hourly'
default_args = {
    'owner': 'Iago'
}

# Reading the hyperparameters of the model
hyperparameters = []
initial_hyperparameter = 3  # First hyperparameter is column index = 3 in the historical dataset
last_hyperparameter = data.shape[1]-5 # Last 5 columns corresponds to performance and train_requested columns
for i in range(initial_hyperparameter, last_hyperparameter):
    hyperparameters.append(filtered_data.iloc[0][i])

# We have to delete the train_requested=TRUE row after reading it.
base_df = data[data['train_requested']!=True].set_index('model')
#base_df.to_csv('/home/iagoaguila/Projects/MLOps_Project/mlops/MLOps_Airflow/shared_volume/historical_validation.csv')
#base_df.to_csv('./shared_volume/historical_validation.csv')


# if dag_id already exists it should return an error: AirflowDagDuplicatedIdException
#try:
    #globals()[dag_id] = create_dag(dag_id,
                                   #schedule,
                                   #default_args,
                                   #hyperparameters)

#except Exception as e:
    #print(e)
    # we should just trigger the existing dag