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
