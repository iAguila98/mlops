import os
import re
import time
import unittest

import pandas as pd

from MLOps_Airflow.dags.scripts.add_data_script import generate_data
from MLOps_Airflow.dags.scripts.preprocessing import preprocessing_pipeline

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/extracted.csv")
path2batchdata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/batch_data_test.csv")
path2events = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/events_dictionary.pkl")
path2snaps = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/snaps_dictionary.pkl")


class DataTests(unittest.TestCase):
    def test_generate_data(self):
        """
        The purpose of this function is to test the 'generate_data' task used by the dataset_creation_dag.py. In order
        to do this, new datasets are used to not affect those running in the main code. We execute the function where
        the new batch data is generated (generate_data) and checks whether specific columns are changed, meaning that
        the new batch is different from the initial data.

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        # Read initial batch data
        initial_batch_data = pd.read_csv(path2batchdata)

        # Execute the function that is tested
        final_batch_data = generate_data(path2batchdata, path2events, path2snaps)

        # Compare the columns that must be different
        compare_date = initial_batch_data['date'].equals(final_batch_data['date'])
        compare_price = initial_batch_data['sell_price'].equals(final_batch_data['sell_price'])
        compare_d = initial_batch_data['d'].equals(final_batch_data['d'])

        # Check if the columns are different
        time.sleep(1)
        self.assertFalse(compare_date)
        self.assertFalse(compare_price)
        self.assertFalse(compare_d)

    def test_preprocessing_pipeline(self):
        """
        The purpose of this function is to test the 'preprocessing_pipeline' function used to preprocess the data after
        adding new rows. We execute the related function and checks whether the preprocessed dataset has any Null value.
        If it has none, it means that the pipeline has been completed, since removing null values is the last step it
        performs.

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """

        # Read initial data
        initial_data = pd.read_csv(path2data)

        # Preprocess data
        pre_data = preprocessing_pipeline(initial_data)

        # Check if there is no Null value in the entire preprocessed dataset
        time.sleep(1)
        self.assertFalse(pre_data.isnull().values.any())
