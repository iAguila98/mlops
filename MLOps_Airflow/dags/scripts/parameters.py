import logging


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
    split_name = model_name.split('_')
    if split_name[0] == 'linear':
        n_jobs = split_name[2]
        if split_name[1] == 'T':
            fit_intercept = True
        if split_name[1] == 'F':
            fit_intercept = False
        else:
            logging.info('Model name not supported')
    else:
        logging.info('Model name not supported')
    parameters = {'fit_intercept': fit_intercept, 'n_jobs': n_jobs}
    return parameters