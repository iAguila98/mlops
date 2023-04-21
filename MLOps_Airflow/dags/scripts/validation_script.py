import pandas as pd

import scripts.custom_metrics as custom_metrics
from scripts.parameters import get_parameters


def validation(model, model_name, eval_path):
    """
    Given a model and a dataset, perform a validation using 4 different metrics.

    Parameters
    ----------
    model: model to validate (loaded pickle)
    model_name: name of the model being evaluated (str)
    eval_path: path to validation dataset (str)

    Returns
    -------
    Dictionary with model name and hyperaparameters, validation metrics and current date. (dict)
    - model: model name that is evaluated. (str)
    - hyperparameters: each hyperparameter is a key.
    - mae, wmape, rmse, tweedie: validation metrics results. (float)
    - val_date: current datetime. (datetime)
    """

    # Read the test set and prepare it
    df = pd.read_csv(eval_path)
    target_col = 'sales'
    test_x = df.drop([target_col, 'date'], axis='columns')
    test_y = df[target_col]

    # Predict and compute the different metrics
    predictions = model.predict(test_x)
    mae = round(custom_metrics.mae_loss(predictions, test_y), 3)
    wmape = round(custom_metrics.wmape_loss(predictions, test_y), 3)
    rmse = round(custom_metrics.rmse_loss(predictions, test_y), 3)
    tweedie = round(custom_metrics.tweedie_loss(test_y, predictions), 3)

    # Get the correspondent parameters of the model_name to save them in the variable 'results'
    parameters = get_parameters(model_name)

    # Save the results
    results = {'model': model_name,
               'fit_intercept': parameters['fit_intercept'],
               'n_jobs': parameters['n_jobs'],
               'max_depth': parameters['max_depth'],
               'max_leaf_nodes': parameters['max_leaf_nodes'],
               'max_features': parameters['max_features'],
               'mae': mae,
               'wmape': wmape,
               'rmse': rmse,
               'tweedie': tweedie,
               'val_date': pd.to_datetime('now', utc=True)}

    return results
