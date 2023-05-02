import re
import os
import time
import unittest

import numpy as np

from MLOps_Airflow.shared_volume.scripts.file_creation import create_dag

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2newfile = os.path.join(base_path, "MLOps_Airflow/shared_volume/tests/")
path2template = os.path.join(base_path, "MLOps_Airflow/shared_volume/scripts/dag_template.py")


class TestDagCreation(unittest.TestCase):

    def test_create_dag(self):
        """
        The purpose of this function is to test the creation of a new dag with the 'create_dag' function. First, we
        initialize the required arguments to then call the function. Finally, we check whether the new python file
        is created (success) or not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """
        # Initialize model_name, hyperparameters and path2filetest (target path)
        model_name = 'linear_test_T_1'
        hyperparameters = [True, 1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        path2filetest = path2newfile + model_name + '.py'

        # Call the create_dag function to create the new dag file
        create_dag(target_path=path2filetest, template_path=path2template,
                   dag_id=model_name, hyperparameters=hyperparameters)

        # Check if the dag file is created
        time.sleep(1)
        self.assertTrue(os.path.exists(path2filetest))
        time.sleep(1)

        # Delete files inside directory
        os.remove(path2filetest)


