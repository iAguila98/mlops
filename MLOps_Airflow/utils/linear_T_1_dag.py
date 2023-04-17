import pickle
import pandas as pd

from sklearn.linear_model import LinearRegression

from scripts.train_script import train
from scripts.evaluate import reg_test


def get_train_df(data_path, train_path):
    """
    """
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    seven_years_ago = pd.to_datetime('now', utc=True).date() - pd.Timedelta(7*365, 'day')  # 7 years earlier
    ten_years_ago = seven_years_ago - pd.Timedelta(3*365, 'day') # 10 years ago
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
    df = pd.read_csv(results_path)
    filtered_df = df[df['train_requested']==True]

    # Realment no és necessari, ja que el DAG es correspon amb el model i es podrien hardcodejar els parameters
    fit_intercept = filtered_df.iloc[0]['fit_intercept']
    n_jobs = filtered_df.iloc[0]['n_jobs']

    model = LinearRegression(fit_intercept=fit_intercept, n_jobs=n_jobs)
    trained_model = train(model, train_path)
    train_date =  pd.to_datetime('now', utc=True)

    # We have to compute the performance with the evaluation script
    results = reg_test(trained_model, eval_path)
    eval_date =  pd.to_datetime('now', utc=True)

    # We have to save write the new instance into the results_path, after dropping the train_request row
    base_df = df[df['train_requested']!=True]
    new_row = {'model': 'linear_T_1', 'eval_date': eval_date, 'train_date': train_date, 'fit_intercept': fit_intercept,
               'n_jobs': n_jobs, 'mae': results['mae'], 'wmape': results['wmape'], 'rmse': results['rmse'],
               'tweedie': results['tweedie'], 'train_requested': False}

    new_df = base_df.append(new_row, ignore_index=True)
    new_df = new_df.set_index('model')
    new_df.to_csv(results_path)

    # Now we save the trained model with his correspondent name
    pickle.dump(model, open(models_path + 'linear_T_1.sav', 'wb'))


# Aquests serien els path oficials pel DAG
#data_path = './shared_volume/old_preprocessed_data.csv'
#train_path = './shared_volume/train_data.csv'
#model_path = './shared_volume/models/linear_T_1.sav'
#results_path = './shared_volume/historical_training.csv'

# Aquests son els path per fer debugging
data_path = '/MLOps_Airflow/shared_volume/old_preprocessed_data.csv'
eval_path = '/MLOps_Airflow/shared_volume/test_data.csv'
train_path = '/MLOps_Airflow/shared_volume/train_data.csv'
results_path = '/MLOps_Airflow/shared_volume/historical_validation.csv'
models_path = '/MLOps_Airflow/shared_volume/models/'

get_train_df(data_path, train_path)
train_model(eval_path, train_path, results_path, models_path)