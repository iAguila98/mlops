import os
import re
import time
import unittest

from sklearn.linear_model import LinearRegression

from MLOps_Airflow.dags.scripts.train_script import train
from MLOps_Airflow.dags.scripts.validation_script import validation

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2traindata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/train_data.csv")
path2testdata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/test_data.csv")


class LinearModelTests(unittest.TestCase):
    def test_train(self):
        """
        The purpose of this function is to test the 'train' function used by the models train dags. In order to do this,
        a new model is defined those running in the main code. After this, the train function is executed and the code
        checks whether ......

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """

        # Define any model to test if the function works correctly
        model = LinearRegression(fit_intercept=True, n_jobs=1)
        initial_state = model.__getstate__()

        # Call the function
        trained_model, train_date = train(model=model, train_path=path2traindata)
        final_state = trained_model.__getstate__()

        # Check if the status of the model changes after calling the train function
        time.sleep(1)
        self.assertNotEqual(initial_state, final_state)

    def test_validation(self):
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

        # Define any model to test if the function works correctly
        model = LinearRegression(fit_intercept=True, n_jobs=1)
        model_name = 'linear_T_1'

        # Execute the function to be tested
        validation(model=model, model_name=model_name, eval_path=path2testdata)


        time.sleep(1)










