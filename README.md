# MLOps

## Introduction

The purpose of this project is to design and develop an MLOps model pipeline that addresses the challenges of 
maintaining reliable and efficient machine learning models in production. The pipeline integrates various practices 
such as data engineering, model management, monitoring, and retraining to ensure the continual improvement of the models.


The proposed framework for this project consists of three main components:

1. A data storage and preprocessing module, which handles the organization and preparation of the data for model training 
and validation.
2. An orchestration module, which coordinates and automates tasks and operations related to model 
management, monitoring, and retraining. 
3. A user-facing dashboard, which provides visibility and control over the pipeline for the user.

Thanks to the help of Airflow, which is a platform that allows scheduling and monitoring workflows,
a certain level of automation of the machine learning cycle is provided. Through this automation, the 
framework has been designed to work as follows:

1. Data Fetching: The framework is based on a regression task with a dataset called M5 Forecasting, which consists of a time series where 
the quantity of units sold of a series of products in different Walmart stores in different states of the USA must be 
predicted. This dataset is initially static, so in order to simulate the input of new data, we have to simulate the 
entry of new data, a series of functions have been developed to add new rows for each passing day. In this way, Airflow 
schedules this task to run every day at a certain time. This task is simply to simulate a more realistic situation, 
since the rows that are added are not realistically fetched, although the new attribute values are decided in a logical 
and justified way. The task that Ariflow executes automatically generates a new batch of data corresponding to the next 
day of the dataset, adds it to the original data and preprocesses it and then divides it into train data and test data.

2. Model Training: The existing models are programmed to retrain themselves automatically every week, taking into 
account the new batches of data that have been added during those days. The user will be able to communicate with
Airflow through a streamlit dashboard, so it can manually retrain the models or even create new ones if necessary.

3. Model Monitoring: Model performance is checked every day with the newest data through a scheduled task in Airflow.
In this case, the task is designed to perform a validation of all existing models, obtaining the value of four different
metrics: MAE, WMAPE, RMSE and Tweedie. The user can instruct Airflow to execute this task via a button on the dashboard 
at any time. The dashboard displays a graph with all models and their metrics over time.

4. Model Management: This functionality offers the user a series of actions on the existing models, all of which must 
be ordered manually. The first one is to pause or activate the automatic training of any of the existing models. 
If paused, the automatic executions will stop occurring, but if a manual training is ordered, they will be reactivated. 
The second is to delete the model, removing it from Airflow and from the registers found in Python. The logs of the 
model in Airflow will not be deleted.


--EXPLICAR QUE EL OBJETIVO NO ES OBTENER BUENOS RESULTADOS, SINO MOSTRAR LA UTILIDAD DE ESTE SET DE HERRAMIENTAS EN ML.
The project focuses on the orchestration part of the workflow and thus the models' performance is not the best. 
To get better results, better models and a better preprocessing pipeline are needed. 

## Quick Start

First of all, clone the repository in your local machine. Docker-compose and docker are needed to run the project. 
Run the following command inside the MLOps_Airflow folder to mount de volumes and raise them in detached mode:

NOTA: Hay que añadir la instalación de los requirements.txt para la parte de frontend.

NOTA 2: Hay que asegurarse de tener permiso de read-write en todos los shell scripts y ficheros dentro del airflow
shared_volume. Esto se hace con la línea de: echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
Esta linea modifica el fichero .env, que en principio ya está correcto y debería funcionar al hacer clone del git.

Para los sh usar el siguiente comando dentro de la carpeta mlops:
find -type f -iname '*.sh' -not -executable -exec chmod +x {} \;

```commandline
docker compose up airflow-init

docker compose up -d --build
```
NOTA --> Comentar que el --build lo que hace es instalar las dependencias necesarias
para los DAGs. En principio se debe hacer solamente la primera vez que se enciende
docker compose.

```commandline
docker build .
```

Finally, we need to run the next command inside mlops folder to initiate the dashboard:
```commandline
streamlit run MLOps_Frontend/Main.py
```

A new tab will be opened in our browser with the dashboard. Once there, we can navigate through it using the sidebar. 

To acces the airflow UI, you need to open the localhost:8080 in a browser. The credentials are set in the 
docker-compose.yaml file, which are:

USER: airflow

PASSWORD: airflow

<!--
## Installation
explicar la instalació dels requirements.txt. Tot pel correr el projecte en local. En principi no fa falta perque
utilitzem docker. -->

## Code Architecture
We have 2 folders:
1. MLOps_Airflow: Is the responsible for all the backend methods, dag functions which retrain and evaluate the models 
are written inside. Furthermore, a shared_volume folder is created when the airflow docker-compose is initialized. 
This folder contains information needed for the frontend to display plots of the performance, check the dag run 
status and others.

2. MLOps_Frontend: Is the responsible for all the dashboard functionality. It contains the code necessary to plot the 
performance of the models and to trigger train and evaluate dags. It also writes the train hyperparameter 
configuration of a model to the shared_volume so de training dag is able to retrieve the information and train a new 
model. 

Finally, some testing is implemented to validate some of the dag's tasks.

## What to change to adapt the farmework to your project

### Change preprocessed data

In this project the preprocessed data used is stored at MLOps_Airflow/shared_volume/preprocessed_data.csv. If you want 
to change de data, you can add your .csv file with this name or use another file name and change it at the 
MLOps_Airflow/dags/dataset_creation_dag.py.

To change the splitting used to create the test and train datasets, you can do it at the 
MLOps_Airflow/dags/dataset_creation_dag.py dag, inside the get_test_df and get_train_df functions.

### Change train script and train new model types

The train script is located at MLOps_Airflow/dags/scripts/train_script.py.

Even if you change the train script, the dashboard won't show new changes to train the models with it. To do so, the 
MLOps_Frontend/pages/Training.py also needs to be changed and implement new cases where the selected model is the one 
wanted. All the streamlit-airflow connection logic can be shared between different model training, so only the 
selecting model logic needs to be implemented.

Furthermore the MLOps_Airflow/shared_volume/dag_template.py train_model function needs to be changed to detect the new 
model type and pass the hyperparameters. Important to note that this hyperparameters need to be dynamic as they will 
be replaced when the create_dag function from MLOps_Airflow/shared_volume/file_creation.py is executed. Finally, this 
create_dag function needs to implement a way to retrieve the hyperparameters selected and add to the replacements 
dictionary the variable name given in the dag_template.py file.

Some other issues may raise as this process couldn't be tested.

### Change test metrics

The validation process is done using MLOps_Airflow/dags/scripts/validation_script.py. To change it, it is important to 
only change the metrics from the results dictionary keeping the other values untouched.

### Other changes

You can delete the data from the MLOps_Airflow/shared_volume/historical_validation.csv as the data stored is just an 
example. But very important, a blank line must be allways present after the last row, or the new data will be appended 
to this last row.

Also, the different /MLOps_Airflow/dags/linear_* dags are examples and if you want to delete them you also have to 
delete the corresponding model in the MLOps_Airflow/shared_volume/models directory.
