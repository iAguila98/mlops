import logging

import numpy as np


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

    # Initialize all hyperparameters from all model types to nan
    fit_intercept = np.nan
    n_jobs = np.nan
    max_depth = np.nan
    max_leaf_nodes = np.nan
    max_features = np.nan

    # Get the model type selected by the user
    model_type = model_name.split('_')

    # Save hyperparameters from linear_regression
    if model_type[0] == 'linear':
        n_jobs = model_type[2]
        if model_type[1] == 'T':
            fit_intercept = True
        elif model_type[1] == 'F':
            fit_intercept = False

    # Save hyperparameters from decision_tree
    elif model_type[0] == 'decision':
        max_depth = model_type[1]
        if model_type[2] == 'N':
            max_leaf_nodes = None
        else:
            max_leaf_nodes = model_type[2]
        if model_type[3] == 'N':
            max_features = None
        else:
            max_features = model_type[3]

    parameters = {'fit_intercept': fit_intercept, 'n_jobs': n_jobs, 'max_depth': max_depth,
                  'max_leaf_nodes': max_leaf_nodes, 'max_features': max_features}
    return parameters
