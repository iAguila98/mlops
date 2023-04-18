import os
import re
import time
import unittest

from MLOps_Airflow.dags.old_dataset_creation_dag import get_test_df, get_train_df

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/preprocessed_data_test.csv")
path2traintest = os.path.join(base_path, "MLOps_Airflow/shared_volume/train_data_test.csv")
path2evaltest = os.path.join(base_path, "MLOps_Airflow/shared_volume/evaluate_data_test.csv")
path2models = os.path.join(base_path, "MLOps_Airflow/shared_volume/models_test/")
path2trainedmodel = os.path.join(path2models, "linear_T_1.sav")
path2historicaltest = os.path.join(base_path, "MLOps_Airflow/shared_volume/historical_validation_test.csv")

class LinearModelTests(unittest.TestCase):
    def test_get_train_df(self):
        """
        The purpose of this function is to test the 'get_train_df' task used by the dataset_creation.py dag. In order
        to do this, new datasets are used to not affect those running in the main code. We execute the function where
        the train dataset is obtained (get_train_df) and checks whether the train dataset is created (success) or
        not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        get_train_df(path2data, path2traintest)

        time.sleep(1)
        self.assertTrue(os.path.exists(path2traintest))

        os.remove(path2traintest)

    def test_get_val_df(self):
        """
        The purpose of this function is to test the 'get_test_df' task used by the dataset_creation.py dag. In order
        to do this, new datasets are used to not affect those running in the main code. We execute the function where
        the test dataset is obtained (get_test_df) and checks whether the train dataset is created (success) or
        not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        get_test_df(path2data, path2evaltest)

        time.sleep(1)
        self.assertTrue(os.path.exists(path2evaltest))

        os.remove(path2evaltest)
