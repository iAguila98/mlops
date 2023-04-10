import logging
import pandas as pd

import scripts.custom_metrics as custom_metrics
from scripts.parameters import get_parameters


# MISSING the Logging configuration to read the INFO while executing.

def validation(model, model_name, eval_path):
    """
    Given a model and a dataset, perform a validation using 4 different metrics.

    Parameters
    ----------
    model: model to validate (loaded pickle)
    eval_path: path to validation dataset (str)

    Returns
    -------
    Dictionary with model name and hyperaparameters, validation metrics and current date. (dict)
    - model: model name that is evaluated. (str)
    - hyperparameters: each hyperparameter is a key.
    - mae, wmape, rmse, tweedie: validation metrics results. (float)
    - val_date: current datetime. (datetime)
    """
    df = pd.read_csv(eval_path)
    target_col = 'sales'
    test_x = df.drop([target_col, 'date'], axis='columns')
    test_y = df[target_col]

    parameters = get_parameters(model_name)

    logging.info('Starting the test evaluation.')
    predictions = model.predict(test_x)
    mae = round(custom_metrics.mae_loss(predictions, test_y), 3)
    wmape = round(custom_metrics.wmape_loss(predictions, test_y), 3)
    rmse = round(custom_metrics.rmse_loss(predictions, test_y), 3)
    tweedie = round(custom_metrics.tweedie_loss(test_y, predictions), 3)
    results = {'model': model_name,
               'fit_intercept': parameters['fit_intercept'],
               'n_jobs': parameters['n_jobs'],
               'mae': mae,
               'wmape': wmape,
               'rmse': rmse,
               'tweedie': tweedie,
               'val_date': pd.to_datetime('now', utc=True)}
    return results