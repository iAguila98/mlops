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

To conclude, the objective of the project focuses on the introduction of automation and orchestration at various stages of the 
machine learning lifecycle. The performance obtained in the models used is not the most optimal, since it would 
require better model training or better data preprocessing. Since this is not the main objective, it has been left 
in the background and the project has been focused on showing the usefulness of this set of tools in production cases.

## Installation and Quick-Start

In order to implement the developed framework, a series of steps must be followed:

1. First of all, download or clone the repository in your local machine. The data files are not included in the
repository since they are too large. Make sure that they exist in the 'MLOps_Airflow/shared_volume/data/' directory. 
These files are 'extracted.csv', 'preprocessed_data.csv', 'test_data.csv' and 'train_data.csv'.


2. Run the following command in the 'mlops' folder to install the required packages:
    ```commandline
    pip install -r requirements.txt
    ```

3. Install docker-compose inside the MLOps_Airflow folder. The download is available for Windows, Linux and Mac at the 
following website: 
    ```url
    https://docs.docker.com/compose/install/
    ```
    To do this on Windows you need the Pro or Student version, although I recommend the Linux installation as it is more 
    straightforward. In this case, it has been done following the steps explained in scenario two (installation of the 
    compose plugin). To follow this scenario, it is necessary to first install Docker Engine, which can be done 
    according to the explanation provided on the following website:
    ```url
    https://docs.docker.com/engine/install/ubuntu/
    ```

4. On Linux, Airflow needs to know your host user id and needs to have group id set to 0. Otherwise, the files 
created in dags, logs and plugins will be created with root user ownership. To make sure, execute the following 
command inside the MLOps_Airflow folder:
    ```commandline
    echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
    ```
    Having downloaded the framework, this step may not be necessary, as all the necessary files exist and have the required 
    permissions. However, executing the command will have no negative consequences, and allows us to ensure that it will 
    work correctly.


5. Make sure that all shell scripts have read and write permissions to allow execution. For that, you can run the following
command in the MLOps_Airflow/shared_volume/coms/ folder:
    ```commandline
    find -type f -iname '*.sh' -not -executable -exec chmod +x {} \;
    ```
    Again, with the download it is possible that the shell scripts already have the permissions configured correctly, 
    but it is a good idea to make sure.


6. Run the following commands in order and inside the MLOps_Airflow folder to initialize Airflow for the first time. 
    ```commandline
    docker compose up airflow-init
    
    docker compose up -d --build
    ```
   The first command initializes Airflow with the docker-compose.yaml configuration. The second command starts Airflow 
   in detached mode and builds the required packages to execute the different scheduled tasks. 


7. Access the Airflow UI by opening 'localhost:8080' in a browser. The credentials are set in the 
docker-compose.yaml file, which are:
    ```credentials
    USER: airflow
    
    PASSWORD: airflow
    ```

8. Finally, we need to run the next command inside 'mlops' folder to initiate the dashboard:
    ```commandline
    streamlit run MLOps_Frontend/Main.py
    ```
    A new tab will be opened in our browser with the dashboard. Once there, we can navigate through it using the sidebar.
    The connection to streamlit will be closed when the terminal where it is running is closed.


9. If you want to close Airflow, you have to execute the following command:
    ```commandline
    docker compose down
    ```
   This command will simply stop Airflow, so that when it is reconnected the last pending scheduled task for each 
   of the files that are scheduled will be executed. Logs of previously executed runs will still exist. To initialize
   Airflow again, you will only need to execute:
    ```commandline
    docker compose up -d
    ```
    On the other hand, if you want to delete the logs, making a complete restart of Airflow, you just have to add 
    the '-v' flag at the final of the command:
    ```commandline
    docker compose down -v
    ```
    If you do this, the next time you start Airflow you will first need to run both commands:
    ```commandline
    docker compose up airflow-init
    
    docker compose up -d
    ```


## Code Architecture
The project is structured in two main folders:
1. MLOps_Airflow: Is the responsible for all the backend methods, dag functions (Airflow tasks) which retrain and 
evaluate the models among other tasks are written inside. Furthermore, you can find the shared_volume folder which 
contains data, models, python scripts and shell files to execute commands. These resources are placed in this folder
because it is the one accessed from the Streamlit dashboard. Calls to certain files or the procurement of different 
information from the dashboard (MLOps_Frontend folder) is done through this folder.


2. MLOps_Frontend: Is the responsible for all the dashboard functionality. It contains the code necessary that organizes
the elements of the different dashboard pages, such as tables showing important information, graphs showing the metrics
of the models performances. It also provides buttons to order different tasks such as training or evaluating a model.
When executing a task, it also informs the user about the state of the running task. To achieve all this access 
different resources in the shared_volume folder inside MLOps_Airflow.