import os
import pandas as pd
import re
import shutil
import time
import unittest

from MLOps_Airflow.dags.linear_T_1 import train_model
from MLOps_Airflow.dags.old_dataset_creation_dag import get_test_df, get_train_df


base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/preprocessed_data_test.csv")
path2traintest = os.path.join(base_path, "MLOps_Airflow/shared_volume/train_data_test.csv")
path2evaltest = os.path.join(base_path, "MLOps_Airflow/shared_volume/evaluate_data_test.csv")
path2models = os.path.join(base_path, "MLOps_Airflow/shared_volume/models_test/")
path2trainedmodel = os.path.join(path2models, "linear_T_1.sav")
path2historicaltest = os.path.join(base_path, "MLOps_Airflow/shared_volume/historical_validation_test.csv")

print(base_path)

class LinearModelTests(unittest.TestCase):
    def test_train_model(self):
        """
        The purpose of this function is to test the 'train' task used by the models train dags. In order to do this,
        new datasets are used to not affect those running in the main code. We execute the function where the train
        dataset is obtained (get_train_df). Then we also execute the function where the test dataset is obtained
        (get_test_df). After this, the train_model function is executed and the code checks whether the model
        has been created (success) or not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        df = pd.DataFrame(columns=['model', 'val_date', 'train_date', 'fit_intercept', 'n_jobs', 'mae', 'wmape', 'rmse',
                                   'tweedie', 'train_requested'])
        df.loc[0] = ['linear_T_1', '2023-01-24', '2023-01-24', True, 1.0, 0.805, 0.957, 1.836, 3.37, False]
        df.to_csv(path2historicaltest)

        get_train_df(path2data, path2traintest)
        get_test_df(path2data, path2evaltest)
        os.mkdir(path2models)

        train_model(path2evaltest, path2traintest, path2historicaltest, path2models)

        time.sleep(1)
        self.assertTrue(os.path.exists(path2trainedmodel))

        os.remove(path2evaltest)
        os.remove(path2traintest)
        os.remove(path2historicaltest)
        shutil.rmtree(path2models)
