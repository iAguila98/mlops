import shutil

from datetime import datetime


def create_dag(target_path, template_path, dag_id, hyperparameters):
    """
    Given the hyperparameters of a model, this function creates a DAG by using a defined template. The dag id
    and the hyperparameters of the model are arguments that replace spaces in the base template to create the final
    python file (DAG).

    Parameters
    ----------
    target_path: indicates where the DAG is saved (DAG folder). (str)
    dag_id: corresponds to the model name encoded by its hyperparameters. (str)
    hyperparameters: list that contains the values of each hyperparameter. (lst)

    Returns
    -------
    Custom python file according to the model and its hyperparameters, created in the DAG folder. (.py)
    """
    # Initially, we go to the first day of the actual month
    input_dt = datetime.now().date()
    first = input_dt.replace(day=1)
    start_date = 'datetime(' + str(first).replace('-0', ', ') + ')'

    # Initialize all possible hyperparameters with 'np.nan' string
    all_hyper = []
    for i in range(0, len(hyperparameters)):
        all_hyper.append('np.nan')

    # Get the type of model selected by the user
    model_type = dag_id.split('_')[0]

    # If it is a linear regressor model, get its hyperparameters
    if model_type == 'linear':
        all_hyper[0] = str(hyperparameters[0])
        all_hyper[1] = str(int(hyperparameters[1]))

    # If it is a decision tree model, get its hyperparameters
    elif model_type == 'decision':
        all_hyper[2] = str(int(hyperparameters[2]))
        # The max_leaf_nodes can be an integer or a string
        if str(hyperparameters[3]) == 'None':
            all_hyper[3] = str(hyperparameters[3])
        else:
            all_hyper[3] = str(int(hyperparameters[3]))
        all_hyper[4] = str(hyperparameters[4])

    # If it is a gradient boosting model, get its hyperparameters
    elif model_type == 'gradient':
        all_hyper[5] = str(hyperparameters[5])
        all_hyper[6] = str(int(hyperparameters[6]))
        all_hyper[7] = str(int(hyperparameters[7]))
        all_hyper[8] = str(hyperparameters[8])

    # There are no more type models implemented
    else:
        raise Exception('Model name not implemented.')

    # Copy the template into the target path
    shutil.copyfile(template_path, target_path)

    # Replace the variables in the created file
    replacements = {'dag_id_model': "'"+dag_id+"'",
                    'fit_intercept_model': all_hyper[0],
                    'n_jobs_model': all_hyper[1],
                    'd_max_depth_model': all_hyper[2],
                    'max_leaf_nodes_model': all_hyper[3],
                    'd_max_features_model': all_hyper[4],
                    'learning_rate_model': all_hyper[5],
                    'n_estimators_model': all_hyper[6],
                    'g_max_depth_model': all_hyper[7],
                    'g_max_features_model': all_hyper[8],
                    'start_date_change': start_date}

    lines = []
    with open(target_path) as infile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            lines.append(line)
    with open(target_path, 'w') as outfile:
        for line in lines:
            outfile.write(line)


