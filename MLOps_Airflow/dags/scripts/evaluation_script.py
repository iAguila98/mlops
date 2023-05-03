import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error, mean_tweedie_deviance, mean_absolute_error


def evaluation(model, model_name, eval_path):
    """
    Given a model and a dataset, perform an evaluation using 4 different metrics.

    Parameters
    ----------
    model: Model to evaluate (loaded pickle)
    model_name: Name of the model being evaluated (str)
    eval_path: Path to test dataset (str)

    Returns
    -------
    Dictionary with model name and hyperaparameters, evaluation metrics and current date. (dict)
    - model: Model name that is evaluated. (str)
    - hyperparameters: Each hyperparameter is a key.
    - mae, wmape, rmse, tweedie: Evaluation metrics results. (float)
    - val_date: Current datetime. (datetime)
    """

    # Read the test set and prepare it
    df = pd.read_csv(eval_path)
    target_col = 'sales'
    test_x = df.drop([target_col, 'date'], axis='columns')
    test_y = df[target_col]

    # Predict and compute the different metrics
    predictions = model.predict(test_x)
    mae = round(mae_loss(predictions, test_y), 3)
    wmape = round(wmape_loss(predictions, test_y), 3)
    rmse = round(rmse_loss(predictions, test_y), 3)
    tweedie = round(tweedie_loss(predictions, test_y), 3)

    # Get the correspondent parameters of the model_name to save them in the variable 'results'
    parameters = get_parameters(model_name)

    # Save the results
    results = {'model': model_name,
               'fit_intercept': parameters['fit_intercept'],
               'n_jobs': parameters['n_jobs'],
               'd_max_depth': parameters['d_max_depth'],
               'max_leaf_nodes': parameters['max_leaf_nodes'],
               'd_max_features': parameters['d_max_features'],
               'learning_rate': parameters['learning_rate'],
               'n_estimators': parameters['n_estimators'],
               'g_max_depth': parameters['g_max_depth'],
               'g_max_features': parameters['g_max_features'],
               'mae': mae,
               'wmape': wmape,
               'rmse': rmse,
               'tweedie': tweedie,
               'eval_date': pd.to_datetime('now', utc=True)}

    return results


def get_parameters(model_name):
    """
    Function that receives a model name and returns the parameters it was trained with.
    Parameters
    ----------
    model_name: Name of the model. (str)

    Returns
    -------
    Dictionary containing the hyperparameters of the model.
    """

    # Initialize all possible hyperparameters with np.nan
    all_hyper = []
    for i in range(0, 9):
        all_hyper.append(np.nan)

    # Get the model type selected by the user
    model_id = model_name.split('_')

    # Save hyperparameters from linear_regression
    if model_id[0] == 'linear':

        # Get possible fit_intercept values (all_hyper[0])
        if model_id[1] == 'T':
            all_hyper[0] = True
        else:
            all_hyper[0] = False

        # Get possible n_jobs values (all_hyper[1])
        all_hyper[1] = model_id[2]

    # Save hyperparameters from decision_tree
    elif model_id[0] == 'decision':
        # Get possible max_depth values (all_hyper[2])
        all_hyper[2] = model_id[1]

        # Get possible max_leaf_node values (all_hyper[3])
        if model_id[2] == 'N':
            all_hyper[3] = 'None'
        else:
            all_hyper[3] = model_id[2]

        # Get possible max_features values (all_hyper[4])
        if model_id[3] == 'N':
            all_hyper[4] = 'None'
        elif model_id[3] == 'a':
            all_hyper[4] = 'auto'
        elif model_id[3] == 's':
            all_hyper[4] = 'sqrt'
        else:
            all_hyper[4] = 'log2'

    # Save hyperparameters from gradient boosting
    elif model_id[0] == 'gradient':

        # Get possible learning_rate values (all_hyper[5])
        if all_hyper != '1':
            for i in range(len(model_id[1])):
                all_hyper[5] = model_id[1]
        else:
            all_hyper[5] = model_id[1]

        # Get possible n_estimators values (all_hyper[6])
        all_hyper[6] = model_id[2]

        # Get possible max_depth values (all_hyper[7])
        all_hyper[7] = model_id[3]

        # Get possible max_features values (all_hyper[8])
        if model_id[4] == 'N':
            all_hyper[8] = 'None'
        elif model_id[3] == 'a':
            all_hyper[8] = 'auto'
        elif model_id[3] == 's':
            all_hyper[8] = 'sqrt'
        else:
            all_hyper[8] = 'log2'

    # There are no more type models implemented
    else:
        raise Exception('Model name not implemented.')

    # Save all parameters in a dictionary
    parameters = {'fit_intercept': all_hyper[0], 'n_jobs': all_hyper[1], 'd_max_depth': all_hyper[2],
                  'max_leaf_nodes': all_hyper[3], 'd_max_features': all_hyper[4], 'learning_rate': all_hyper[5],
                  'n_estimators': all_hyper[6], 'g_max_depth': all_hyper[7], 'g_max_features': all_hyper[8]}

    return parameters


def mae_loss(predictions, true):
    return mean_absolute_error(predictions, true)


def wmape_loss(predictions, true):
    return np.mean(np.abs(true - predictions)) / np.mean(true)


def rmse_loss(predictions, true):
    return np.sqrt(mean_squared_error(predictions, true))


def tweedie_loss(predictions, true):
    return mean_tweedie_deviance(true, predictions)
