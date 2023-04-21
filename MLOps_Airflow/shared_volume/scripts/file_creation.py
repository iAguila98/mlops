import shutil

from datetime import datetime, timedelta


def create_dag(target_path, dag_id, hyperparameters):
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

    # Define template
    dag_template_file = 'MLOps_Airflow/shared_volume/scripts/dag_template.py'

    # Hyperparameters according to the type of model
    model_type = dag_id.split('_')[0]
    if model_type == 'linear':
        fit_intercept = str(hyperparameters[0])
        n_jobs = str(hyperparameters[1])
    elif model_type == 'decision':
        max_depth = str(hyperparameters[2])
        max_leaf_nodes = str(hyperparameters[3])
        max_features = str(hyperparameters[4])


    print(max_depth, max_leaf_nodes, max_features)
    '''
    # Copy the template into the target path
    shutil.copyfile(dag_template_file, target_path)

    # Replace the variables in the created file
    replacements = {'dag_id_model': "'"+dag_id+"'",
                    'fit_intercept_model': fit_intercept,
                    'n_jobs_model': n_jobs,
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
    '''

