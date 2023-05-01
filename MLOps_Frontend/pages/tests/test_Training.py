import unittest
import re
import os

from MLOps_Frontend.pages.Training import load_data, get_last_model_row

base_path = re.search(r'.+(mlops)', os.getcwd())[0]
path2data = os.path.join(base_path, "MLOps_Airflow/shared_volume/historical_dataset.csv")
path2models = os.path.join(base_path, "MLOps_Airflow/shared_volume/models/")


class TrainingTests(unittest.TestCase):
    def test_get_last_model_row(self):
        """
        See if the get_last_model_row function returns a dataframe with the same number of rows as the number of models.
        """
        historical_df = load_data(path2data)
        last_row_df = get_last_model_row(historical_df)
        model_number = len(os.listdir(path2models))
        self.assertEqual(len(last_row_df.index), model_number)


if __name__ == '__main__':
    unittest.main()
