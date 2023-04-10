# MLOps

## Introduction

The aim of this project is to train and monitor IA model performance through a dashboard. The user will be able to manually train and evaluate the models though automatization  is implemented in the following way:

Model performance is checked every day with the newest data, and the models are retrained every month with newer data using airflow. The user will be able to comunicate with the airflow backend through a streamlit dashboard wich is used to view the model performance and trigger the training of the models.

The project focuses on the orchestration part of the workflow and thus the models' performance is not the best. To get better results, better models and a better preprocessing pipeline are needed. 

## Quick Start

First of all, clone the repository in your local machine. Docker-compose and docker are needed to run the project. Run the following command inside the MLOps_Airflow folder to mount de volumes and raise them in detached mode:

NOTA: Hay que añadir la instalación de los requirements.txt para la parte de frontend.

NOTA 2: Hay que asegurarse de tener permiso de read-write en todos los shell scripts y ficheros dentro del airflow
shared_volume. Esto se hace con la línea de: echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
Esta linea modifica el fichero .env, que en principio ya está correcto y debería funcionar al hacer clone del git.

Para los sh usar el siguiente comando dentro de la carpeta mlops:
find -type f -iname '*.sh' -not -executable -exec chmod +x {} \;

WARNING: Este ultimo comando es peligroso al dar permisos a todos los usuarios, pero en este caso solamente tenemos 
1 usuario que controle la aplicación. Es necesario porque el creador de estos ficheros es el usuario del airflow, el 
cual es diferente al usuario que controla el frontend (el personal). Entonces detecta que no somos el creador y que no
podemos darle permisos. Como no se puede cambiar de creador por temas de funcionalidad, entonces se aplica el comando
mencionado.

```commandline
docker compose up airflow-init

docker compose up -d
```
WARNING: A mi el docker build ., no me ha hecho falta. Posiblemente porque ya está implícito en el docker-compose
Once it finishes, install python dependencies needed as follows:

```commandline
docker build .
```

Finally, we need to run the next command inside mlops folder to initiate the dashboard:
```commandline
streamlit run MLOps_Frontend/Main.py
```

A new tab will be opened in our browser with the dashboard. Once there, we can navigate through it using the sidebar. 

To acces the airflow UI, you need to open the localhost:8080 in a browser and the credentials are set in the docker-compose.yaml file, which are user: airflow; password: airflow.
<!--
## Installation
explicar la instalació dels requirements.txt. Tot pel correr el projecte en local. En principi no fa falta perque
utilitzem docker. -->

## Code Architecture
We have 2 folders:
1. MLOps_Airflow: Is the responsible for all the backend methods, dag functions which retrain and evaluate the models are written inside. Furthermore, a shared_volume folder is created when the airflow docker-compose is initialized. This folder contains information needed for the frontend to display plots of the performance, check the dag run status and others.

2. MLOps_Frontend: Is the responsible for all the dashboard functionality. It contains the code necessary to plot the performance of the models and to trigger train and evaluate dags. It also writes the train hyperparameter configuration of a model to the shared_volume so de training dag is able to retrieve the information and train a new model. 

Finally, some testing is implemented to validate some of the dag's tasks.

## What to change to adapt the farmework to your project

### Change preprocessed data

In this project the preprocessed data used is stored at MLOps_Airflow/shared_volume/preprocessed_data.csv. If you want to change de data, you can add your .csv file with this name or use another file name and change it at the MLOps_Airflow/dags/dataset_creation_dag.py.

To change the splitting used to create the test and train datasets, you can do it at the MLOps_Airflow/dags/dataset_creation_dag.py dag, inside the get_test_df and get_train_df functions.

### Change train script and train new model types

The train script is located at MLOps_Airflow/dags/scripts/train_script.py.

Even if you change the train script, the dashboard won't show new changes to train the models with it. To do so, the MLOps_Frontend/pages/Training.py also needs to be changed and implement new cases where the selected model is the one wanted. All the streamlit-airflow connection logic can be shared between different model training, so only the selecting model logic needs to be implemented.

Furthermore the MLOps_Airflow/shared_volume/dag_template.py train_model function needs to be changed to detect the new model type and pass the hyperparameters. Important to note that this hyperparameters need to be dynamic as they will be replaced when the create_dag function from MLOps_Airflow/shared_volume/file_creation.py is executed. Finally, this create_dag function needs to implement a way to retrieve the hyperparameters selected and add to the replacements dictionary the variable name given in the dag_template.py file.

Some other issues may raise as this process couldn't be tested.

### Change test metrics

The validation process is done using MLOps_Airflow/dags/scripts/validation_script.py. To change it, it is important to only change the metrics from the results dictionary keeping the other values untouched.

### Other changes

You can delete the data from the MLOps_Airflow/shared_volume/historical_validation.csv as the data stored is just an example. But very important, a blank line must be allways present after the last row, or the new data will be appended to this last row.

Also the different /MLOps_Airflow/dags/linear_* dags are examples and if you want to delete them you also have to delete the corresponding model in the MLOps_Airflow/shared_volume/models directory.
