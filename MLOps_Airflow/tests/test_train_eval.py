import os
import re
import time
import unittest

import numpy as np

from sklearn.linear_model import LinearRegression

from MLOps_Airflow.dags.scripts.train_script import train
from MLOps_Airflow.dags.scripts.evaluation_script import evaluation

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2traindata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/train_data.csv")
path2testdata = os.path.join(base_path, "MLOps_Airflow/shared_volume/data/test_data.csv")


class LinearModelTests(unittest.TestCase):
    def test_train(self):
        """
        The purpose of this function is to test the 'train' function used by the models train dags. In order to do this,
        a new model is defined to avoid using those running in the main code. After this, the train function is executed
        and the code checks whether the initial state of the model changes after the training (success) or not (failed).

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

    def test_evaluation(self):
        """
        The purpose of this function is to test the 'validation' function used in a task from the evaluation_dag.py. In
        order to do this, a new model is defined and trained to avoid using those running in the main code. We execute
        the function where the prediction is obtained (validation). The results are returned by the function and checked
        checks in order to know if the prediction has been performed. Specifically, we check whether it returns the
        metric values (success) or not (failed).

        Returns
        -------
        Boolean shown in the terminal. True if test is successful / False if test has failed.
        """

        # Define any model to test if the function works correctly
        model = LinearRegression(fit_intercept=True, n_jobs=1)
        model_name = 'linear_T_1'

        # Train the model before validate it
        trained_model, train_date = train(model=model, train_path=path2traindata)

        # Execute the function to be tested
        results = evaluation(model=trained_model, model_name=model_name, eval_path=path2testdata)
        metrics = list(results)[-5:-1]

        # Save each value metric from the results dictionary
        values = []
        for key in results:
            if key in metrics:
                values.append(results[key])

        # Check if there are any nan in the metrics results
        time.sleep(1)
        self.assertFalse(np.isnan(values).any())










