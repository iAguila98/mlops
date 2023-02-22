import os
import time
import unittest

from MLOps_Airflow.shared_volume.file_creation import create_dag


class TestDagCreation(unittest.TestCase):

    def test_create_dag(self):
        """
        The purpose of this function is to test the creation of a new dag with the 'create_dag' function. First, we
        initialize the required arguments to then call the function. Finally, we check whether the train dataset
        is created (success) or not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        # Initialize hyperparameters, model_name and path2filetest (target path)
        model_name = 'lineartest_T_1'
        hyperparameters = [True, 1]  # Indicates fit_intercept and n_jobs
        path2filetest = 'MLOps_Airflow/shared_volume/' + model_name + '.py'

        create_dag(path2filetest, model_name, hyperparameters)

        time.sleep(1)
        self.assertTrue(os.path.exists(path2filetest))
        time.sleep(1)

        # Delete files inside directory.
        os.remove(path2filetest)


