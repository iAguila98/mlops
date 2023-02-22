import streamlit as st
from PIL import Image

# Web configuration
st.set_page_config(
    initial_sidebar_state="auto",
    layout='wide'
)

logo_url = 'data:image/png;base64,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'
st.image(logo_url, width=250)
st.title('The MLOps Experience')

st.subheader('Contributors')

col1, col2, col3, col4 = st.columns(4)
with col1:
    image = Image.open('MLOps_Frontend/images/pau.jpg')
    st.image(image, caption='Pau Coll', width=300)
with col2:
    image = Image.open('MLOps_Frontend/images/iago.jpg')
    st.image(image, caption='Iago Águila', width=300)
with col3:
    image = Image.open('MLOps_Frontend/images/tania.jpg')
    st.image(image, caption='Tania Klymchuk', width=300)
with col4:
    image = Image.open('MLOps_Frontend/images/marc.jpg')
    st.image(image, caption='Marc Alvinyà', width=300)

st.subheader('MLOps Introduction')

st.markdown('<div style="text-align: justify;"><font size=5> MLOps, or Machine Learning Operations, is an extension of the DevOps '
            'methodology that seeks to include machine learning and data science processes in the development and '
            'operations chain to make ML development more reliable and productive. The objective of MLOps is to develop'
            ', train and deploy ML models with automated procedures. It also offers communication and collaboration '
            'between data scientists while automating and productizing machine learning algorithms.</font></div>',
            unsafe_allow_html=True)

st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> In order to use models in production environments, they have to be '
            'updated and maintained. It is therefore vital that the efforts and times for their deployment and '
            'maintenance are reduced as much as possible. This is the advantage that makes MLOps an important '
            'framework. </font></div>', unsafe_allow_html=True)

for i, col in enumerate(st.columns(4)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/MLops.png')
            st.image(image, caption='MLOps Framework', width=700)
    else:
        with col:
            st.write('')

st.subheader('Dataset introduction')

st.markdown('<div style="text-align: justify;"><font size=5>The framework developed throughout the experience aims to simulate a '
            'pre-production environment where the reliability and maintenance of the models is performed automatically,'
            ' but can also be controlled by the user himself. The models will be trained and evaluated on a specific '
            'dataset called M5 Forecasting. This dataset, which is a time series, consists of estimating the point '
            'forecasts of the unit sales of various products sold in the USA by Walmart. In order to train and evaluate'
            ' the models, a data engineering exercise was previously performed by analyzing the dataset and building '
            'a preprocessing pipeline. </font></div>', unsafe_allow_html=True)

st.write('')


for i, col in enumerate(st.columns(4)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/M5.png')
            st.image(image, caption='M5 Dataset Structure', width=700)
    else:
        with col:
            st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> The dataset stores the number of units sold of each of the products '
            'for each day from 2011 to 2016. These records are unique for each of the stores that exist in the three'
            ' states. Therefore, the target variable is the unit of products sold for each store in each state. In'
            ' our case, the dataset has been reduced by selecting only the first store for each state. </font></div>'
            , unsafe_allow_html=True)

st.write('')

for i, col in enumerate(st.columns(4)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/dataset.png')
            st.image(image, caption='Example Features of M5 Dataset', width=800)
    else:
        with col:
            st.write('')


st.markdown("""<font size=5>The proposed MLOps framework consists of three main blocks:</font>""", unsafe_allow_html=True)

st.subheader('Data storage and preprocessing module') 

st.markdown('<div style="text-align: justify;"><font size=5> First of all, the data storage'
            ' stores the preprocessed data locally. Since the dataset we are working with is static (it does not add '
            'instances over time), the preprocessing is executed only once. In this way, the preprocessed dataset is '
            'saved and worked with in the developed MLOps environment. But in a real environment, it would be a data '
            'warehowse that gets updated daily or somthing similar'
            ' </font></div>', unsafe_allow_html=True)

st.subheader('Orchestration module') 

st.markdown('<div style="text-align: justify;"><font size=5> The orchestration module schedules and triggers different tasks like '
            'training a new model, retraining or evaluating. It also controls a dataset task that is based on updating '
            'the training set and test set from the current day (sliding window over time). We avoid using the full '
            'dataset due to computational resources but also to take advantage and get a simulation of a dataset that '
            'changes over time.'
            ' </font></div>', unsafe_allow_html=True)

st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> In our case we used airflow. It is an orchestrator '
            'which uses DAGs (Directed Asyclic Graph) to monitor and schedule tasks. Each task works independently and '
            'the execution of the DAG can be shceduled using cron expressions. Furthermore, sensors can be used to '
            'detect the execution status of previous DAGs and build more complex applications. '
            ' </font></div>', unsafe_allow_html=True)

st.write('')

for i, col in enumerate(st.columns(6)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/dag_example.png')
            st.image(image, caption='Example of an airflow DAG', width=800)
    else:
        with col:
            st.write('')

st.subheader('Dashboard') 

st.markdown('<div style="text-align: justify;"><font size=5> Using the dashboard, the user will be able to manually train models with'
            ' new hyperparameters, retrain existing models, evaluate the performance of different models, and monitor'
            ' the performance of the deployed models in the simulated pre-production environment. The dashboard will'
            ' also facilitate the visualization of the performance metrics of the models, making it easy for the user'
            ' to identify any issues or opportunities for improvement. '
            ' </font></div>', unsafe_allow_html=True)

st.write('')
st.write('')
st.write('')


st.markdown('<div style="text-align: justify;"><font size=5> So as you can see, to implement this framework we used python, airflow, docker, and '
            'streamlit. Python is used for building the pipeline and the preprocessing pipeline, airflow for '
            'scheduling and orchestration of the pipeline, docker for the containerization of airflow, and streamlit for building '
            'the user dashboard. The communication between the dashboard (streamlit) and the orchestration module '
            '(airflow) is one of the most important challenges of this experience.'
            ' </font></div>', unsafe_allow_html=True)

st.write('')

st.subheader('Application Workflow')

st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> In this section you can see a series of diagrams that explain the '
            'workflow of the application. Specifically, the diagrams show the operation of the Airflow DAGs and also'
            ' the operation of the streamlit (dashboard). The latter shows the workflow of the code behind the'
            ' activation of each button. These procedures involve communication with Airflow which is generally'
            ' done from a shared docker volume. For now, the dashboard is not a docker container, but as future'
            ' work is one of the tasks to be considered.'
            ' </font></div>', unsafe_allow_html=True)

st.write('')

for i, col in enumerate(st.columns(6)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/data_dag.png')
            st.image(image, caption='Dataset Creation DAG in Airflow', width=800)
    else:
        with col:
            st.write('')

st.write('')

for i, col in enumerate(st.columns(6)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/val_dag.png')
            st.image(image, caption='Validation DAG in Airflow', width=800)
    else:
        with col:
            st.write('')

st.write('')

for i, col in enumerate(st.columns(6)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/train_dag.png')
            st.image(image, caption='Training DAG in Airflow', width=800)
    else:
        with col:
            st.write('')

st.write('')

for i, col in enumerate(st.columns(13)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/streamlit.png')
            st.image(image, caption='Validation DAG in Airflow', width=1100)
    else:
        with col:
            st.write('')

st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> From the streamlit diagram we can see that when training a model it '
            'may or may not exist. In case it does not exist, a .py file is generated from a template in order to '
            'create a new DAG for that specific model. This can be called dynamic creation of DAGs, since when using '
            'Airflow in the most basic way the DAGs are static .py files. '
            ' </font></div>', unsafe_allow_html=True)

st.write ('')

st.markdown('<div style="text-align: justify;"><font size=5> During the dynamic DAG creation procedure, the first thing the code '
            'does is the creation of the new .py file according to the characteristics of the requested model. '
            'Afterwards, it enters a loop where a request is made to the Airflow Rest API. This request asks for '
            'information about the DAG, which will only be obtained when it exists. When it detects that it already '
            'exists, the trigger is performed on this DAG. When the user wants to check the status of the trigger, '
            'another request to the Rest API will be made using the id of the executed trigger.'
            ' </font></div>', unsafe_allow_html=True)

st.write('')

st.markdown('<div style="text-align: justify;"><font size=5> The trigger status check is prepared to receive a series of states '
            'from the DAG run: running, success and failed. These are the states we expect according to the '
            'functionality of the application, but there can always be other states outside of these. An example is '
            'queued, which happens when there is a previous execution that has not yet finished. In these cases, a '
            'message will appear to the user informing about the situation and advising to check what happened in '
            'the Airflow webserver. This is a case of error handling of the application, although as future work '
            'we would consider adding more cases (e.g., timeout when waiting for the detection of a new created DAG).'
            ' </font></div>', unsafe_allow_html=True)
