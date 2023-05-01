import os
import re
import time
import unittest

import pandas as pd

from MLOps_Airflow.dags.dataset_creation_dag import add_data

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/extracted_test.csv")
path2batchdata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/batch_data_test.csv")
path2events = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/events_dictionary.pkl")
path2snaps = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/snaps_dictionary.pkl")

# WE SHOULD TEST THE GENERATE DATA INSTEAD OF ADD_DATA porque no me deja completar el test ya que usa una funcion que
# está en otra carpeta

class DataTests(unittest.TestCase):
    def test_add_data(self):
        """
        The purpose of this function is to test the 'add_data' task used by the dataset_creation_dag.py. In order
        to do this, new datasets are used to not affect those running in the main code. We execute the function where
        the original data is modified and the new batch data is saved (add_data) and checks whether the datasets are
        created or not.

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        # Read initial test data
        initial_data = pd.read_csv(path2data)
        initial_len = len(initial_data.index)

        # Execute the function that is tested
        add_data(path2data, path2batchdata, path2events, path2snaps)

        # Read the updated data
        final_data = pd.read_csv(path2data)
        final_len = len(final_data.index)

        # Go back to the initial test data
        initial_data.to_csv(path2data)

        # Check if the conditions are True
        time.sleep(1)
        self.assertTrue(os.path.exists(path2batchdata))
        self.assertNotEqual(initial_len, final_len)

        # Remove the batch data generated
        os.remove(path2batchdata)

'''
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
'''