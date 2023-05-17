import streamlit as st
from PIL import Image

# Web configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto"
)

logo_url = "data:image/png;base64,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"
st.image(logo_url, width=500)
st.title('Main page')

st.markdown('<div style="text-align: justify;"><font size=3> It is recommended to use a resolution of 1920x1080 for a '
            'correct visualization. </font></div>', unsafe_allow_html=True)

st.subheader('MLOps Introduction')

st.markdown('<div style="text-align: justify;"><font size=3> MLOps, or Machine Learning Operations, is an extension of '
            'the DevOps methodology that seeks to include machine learning and data science processes in the '
            'development and operations chain to make ML development more reliable and productive. The objective of '
            'MLOps is to develop, train and deploy ML models with automated procedures. It also offers communication '
            'and collaboration between data scientists while automating and productizing machine learning '
            'algorithms.</font></div>', unsafe_allow_html=True)

st.write('')

st.markdown('<div style="text-align: justify;"><font size=3> In order to use models in production environments, they '
            'have to be updated and maintained. It is therefore vital that the efforts and times for their deployment '
            'and maintenance are reduced as much as possible. This is the advantage that makes MLOps an important '
            'framework. </font></div>', unsafe_allow_html=True)

for i, col in enumerate(st.columns(4)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/MLops.png')
            st.image(image, caption='MLOps Framework', width=600)
    else:
        with col:
            st.write('')

st.subheader('Dataset')

st.markdown('<div style="text-align: justify;"><font size=3>The MLOps pipeline developed aims to simulate a '
            'pre-production environment where the reliability and maintenance of the models is performed automatically,'
            ' but where some functionalities can also be manually controlled by the user. The models will be trained '
            'and evaluated on a specific dataset called M5 Forecasting. This dataset, which is a time series, consists '
            'of estimating the point forecasts of the unit sales of various products sold in the USA by Walmart. '
            '</font></div>', unsafe_allow_html=True)

st.write('')


for i, col in enumerate(st.columns(5)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/M5.png')
            st.image(image, caption='M5 Dataset Structure', width=700)
    else:
        with col:
            st.write('')

st.markdown('<div style="text-align: justify;"><font size=3> The dataset stores the number of units sold of each of '
            'the products for each day from 2011 to 2016. These records are unique for each of the stores that exist '
            'in the three states. Therefore, the target variable is the unit of products sold for each store in each '
            'state. For this case, the dataset has been reduced by selecting only the first store for each state. '
            '</font></div>', unsafe_allow_html=True)

st.write('')

for i, col in enumerate(st.columns(5)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/dataset.png')
            st.image(image, caption='Example Features of M5 Dataset', width=800)
    else:
        with col:
            st.write('')

st.subheader('Developed MLOps Framework')

st.markdown("""<font size=3>The proposed MLOps framework consists of three main blocks: Data Generation and 
Preparation, Orchestration and Dashboard. </font>""", unsafe_allow_html=True)

st.markdown('<div style="text-align: justify;"><font size=3> DATA GENERATION AND PREPARATION: The data generation and '
            'preparation system basically simulates the growth of the dataset with new data over time. The original '
            'dataset is static, so new data is not being generated. To create an MLOps framework and show its '
            'usefulness, it has been decided to simulate this input of new data. The data generation and preparation '
            'process is responsible for generating and preprocessing a new data batch corresponding to a new day of '
            'the week. The values of some of the feature are generated with respect to the original data and others '
            'with respect to the data of the last recorded day, following justified guidelines. Thanks to data '
            'generation and preparation, it will be possible to appreciate the change in the performance of the '
            'models as they are monitored. </font></div>', unsafe_allow_html=True)

st.write('')

st.markdown('<div style="text-align: justify;"><font size=3> ORCHESTRATION: The orchestration module schedules and '
            'triggers different tasks like training a new model, retraining or evaluating. It also controls the data '
            'generation and preparation functionality, where one batch of new data is generated and preprocessed each '
            'day of the week. In this case, Airflow has been used as the orchestrator module. It is an orchestrator '
            'which uses DAGs (Directed Acyclic Graph) to monitor and schedule tasks. Each task works independently and '
            'the execution of the DAG can be scheduled using cron expressions. Furthermore, sensors can be used to '
            'detect the execution status of previous DAGs and build more complex applications. '
            '</font></div>', unsafe_allow_html=True)

st.write('')

for i, col in enumerate(st.columns(5)):
    if i == 1:
        with col:
            image = Image.open('MLOps_Frontend/images/dag_example.png')
            st.image(image, caption='Example of an airflow DAG', width=700)
    else:
        with col:
            st.write('')

st.markdown('<div style="text-align: justify;"><font size=3> DASHBOARD: Using the dashboard, the user will be able to '
            'check information about the status of the models and its performances over time. It also allows to order'
            'different tasks manually through the use of buttons. These tasks are: train/retrain models, evaluate '
            'models, pause/activate continuous training of models and delete models. The dashboard is divided into'
            'four pages: Main (current page), Managing Models, Monitoring Models and Training Models. Feel free to '
            'explore the pages and interact with them. Pay attention to the messages that the dashboard offers '
            'in different situations. </font></div>', unsafe_allow_html=True)
