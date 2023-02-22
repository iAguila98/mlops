import os
import pickle
import pandas as pd
import re
import time
import unittest

from sklearn.linear_model import LinearRegression

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/preprocessed_data_test.csv")
path2evaltest = os.path.join(base_path, "MLOps_Airflow/shared_volume/evaluate_data_test.csv")
path2modelstest = os.path.join(base_path, 'MLOps_Airflow/shared_volume/test_models/')
path2historicaltest = os.path.join(base_path, 'MLOps_Airflow/shared_volume/historical_validation_test.csv')

os.chdir(os.path.join(base_path, "MLOps_Airflow/dags/scripts"))
os.getcwd()

from MLOps_Airflow.dags.validation_dag import get_test_df
from MLOps_Airflow.dags.validation_dag import evaluate

class LinearModelTests(unittest.TestCase):
    def test_evaluate(self):
        """
        The purpose of this function is to test the 'evaluate' task used by validation_dag.py. In order to do this,
        new datasets are used so as not to affect those running in the main code. We execute the function where the
        test dataset is obtained (get_test_df). Any model is trained with this same dataset and is saved to later
        execute the function 'evaluate', which is the one to be tested. The results are saved in the historical test
        dataset and checks if they have indeed been added (success) or not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        # First, we get the evaluation test dataset
        get_test_df(path2data, path2evaltest)

        # Create a directory where the test model will be saved
        os.mkdir(path2modelstest)

        # Save a test model to perform the testing
        test_model = LinearRegression(fit_intercept=True, n_jobs=1.0)
        df = pd.read_csv(path2evaltest) # Trained with the validation set in order to avoid extra computation
        target_col = 'sales'
        train_x = df.drop([target_col, 'date'], axis='columns')
        train_y = df[target_col]
        test_trained_model = test_model.fit(train_x, train_y)
        pickle.dump(test_trained_model, open(path2modelstest + 'linear_T_1' + '.sav', 'wb'))

        # Create the historical dataset test
        df = pd.DataFrame(columns=['model','val_date','train_date','fit_intercept','n_jobs','mae','wmape','rmse',
                                   'tweedie','train_requested'])

        # It is necessary to have a row that corresponds to the model evaluated
        df.loc[0] = ['linear_T_1','2023-01-24','2023-01-24',True,1.0,0.805,0.957,1.836,3.37,False]
        df.to_csv(path2historicaltest)

        # Save the initial length of the historical csv
        historical_df = pd.read_csv(path2historicaltest)
        historical_len_1 = len(historical_df.index)

        # Execute the function to be tested with the new arguments (test arguments)
        evaluate(path2modelstest, path2evaltest, path2historicaltest)
        time.sleep(1)

        # Check if new rows have been added in the historical validation test csv.
        historical_df = pd.read_csv(path2historicaltest)
        historical_len_2 = len(historical_df.index)
        self.assertNotEqual(historical_len_1, historical_len_2)

        # The evaluation test dataset is deleted
        os.remove(path2modelstest + 'linear_T_1' + '.sav')
        os.rmdir(path2modelstest)
        os.remove(path2historicaltest)
        os.remove(path2evaltest)
