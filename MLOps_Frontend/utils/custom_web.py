import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

from sklearn.metrics import mean_squared_error, mean_tweedie_deviance, mean_absolute_error


def mae_loss(predictions, true):
    return mean_absolute_error(predictions, true)


def wmape_loss(predictions, true):
    return np.mean(np.abs(true - predictions)) / np.mean(true)


def rmse_loss(predictions, true):
    return np.sqrt(mean_squared_error(predictions, true))


def tweedie_loss(predictions, true):
    return mean_tweedie_deviance(true, predictions)


def splitting(dataset):
    test_set = dataset[dataset['date'] >= '2015-05-22']
    val_set = dataset[(dataset['date'] >= '2014-05-22')
                           & (dataset['date'] < '2015-05-22')]
    training_set = dataset[dataset['date'] < '2014-05-22']

    test_X = test_set.drop(['sales', 'date'], axis=1)
    test_y = test_set['sales']
    val_X = val_set.drop(['sales', 'date'], axis=1)
    val_y = val_set['sales']
    train_X = training_set.drop(['sales', 'date'], axis=1)
    train_y = training_set['sales']

    return train_X, train_y, val_X, val_y, test_X, test_y


def reg_global_analysis(**kwargs):
    predictions = kwargs['model'].predict(kwargs['val_X'])
    true = kwargs['val_y']

    mae = round(mae_loss(predictions, true), 3)
    wmape = round(wmape_loss(predictions, true), 3)
    rmse = round(rmse_loss(predictions, true), 3)
    tweedie = round(tweedie_loss(predictions, true), 3)
    return mae, wmape, rmse, tweedie

def reg_sales_analysis(**kwargs):
    predictions = kwargs['model'].predict(kwargs['val_X'])
    true = kwargs['val_y']

    true = true.reset_index(drop=True)
    true_big_sales = true[true > kwargs['big_sales']]
    true_low_sales = true[true <= kwargs['big_sales']]
    true_values = [true_big_sales, true_low_sales]
    mae, wmape, rmse, tweedie = ([], [], [], [])

    for true in true_values:
        indexes = true.index
        sales_predictions = [predictions[i] for i in indexes]

        sales_mae = round(mae_loss(sales_predictions, true), 3)
        mae.append(sales_mae)

        sales_wmape = round(wmape_loss(sales_predictions, true), 3)
        wmape.append(sales_wmape)

        sales_rmse = round(rmse_loss(sales_predictions, true), 3)
        rmse.append(sales_rmse)

        sales_tweedie = round(tweedie_loss(sales_predictions, true), 3)
        tweedie.append(sales_tweedie)

    return mae, wmape, rmse, tweedie

def reg_categories_analysis(**kwargs):
    predictions = kwargs['model'].predict(kwargs['val_X'])
    true = kwargs['val_y']

    data = kwargs['val_X'].reset_index(drop=True)
    categories = ['cat_id_FOODS', 'cat_id_HOBBIES', 'cat_id_HOUSEHOLD']
    mae, wmape, rmse, tweedie = ([], [], [], [])

    for cat in categories:
        index = data[data[cat] == 1].index
        cat_true = true.iloc[index]
        cat_predictions = [predictions[i] for i in index]

        cat_mae = round(mae_loss(cat_predictions, cat_true), 3)
        mae.append(cat_mae)

        cat_wmape = round(wmape_loss(cat_predictions, cat_true), 3)
        wmape.append(cat_wmape)

        cat_rmse = round(rmse_loss(cat_predictions, cat_true), 3)
        rmse.append(cat_rmse)

        cat_tweedie = round(tweedie_loss(cat_predictions, cat_true), 3)
        tweedie.append(cat_tweedie)

    return mae, wmape, rmse, tweedie


def reg_states_analysis(**kwargs):
    predictions = kwargs['model'].predict(kwargs['val_X'])
    true = kwargs['val_y']

    data = kwargs['val_X'].reset_index(drop=True)
    states = ['state_id_CA', 'state_id_TX', 'state_id_WI']
    mae, wmape, rmse, tweedie = ([], [], [], [])

    for sta in states:
        index = data[data[sta] == 1].index
        sta_true = true.iloc[index]
        sta_predictions = [predictions[i] for i in index]

        sta_mae = round(mae_loss(sta_predictions, sta_true), 3)
        mae.append(sta_mae)

        sta_wmape = round(wmape_loss(sta_predictions, sta_true), 3)
        wmape.append(sta_wmape)

        sta_rmse = round(rmse_loss(sta_predictions, sta_true), 3)
        rmse.append(sta_rmse)

        sta_tweedie = round(tweedie_loss(sta_predictions, sta_true), 3)
        tweedie.append(sta_tweedie)

    return mae, wmape, rmse, tweedie


def show_sales_analysis(**kwargs):
    selected_metrics = kwargs['selected_metrics']
    mae = kwargs['mae']
    wmape = kwargs['wmape']
    rmse = kwargs['rmse']
    tweedie = kwargs['tweedie']

    cols = st.columns(4)
    for i, metric in enumerate(selected_metrics):
        if metric == 'MAE':
            with cols[i]:
                df = pd.DataFrame({
                    'Sale Type': ['Big Sales', 'Low Sales'],
                    'MAE': mae
                })
                fig = px.bar(df, x='Sale Type', y='MAE',
                             title='MAE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'WMAPE':
            with cols[i]:
                df = pd.DataFrame({
                    'Sale Type': ['Big Sales', 'Low Sales'],
                    'WMAPE': wmape
                })
                fig = px.bar(df, x='Sale Type', y='WMAPE',
                             title='WMAPE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'RMSE':
            with cols[i]:
                df = pd.DataFrame({
                    'Sale Type': ['Big Sales', 'Low Sales'],
                    'RMSE': rmse
                })
                fig = px.bar(df, x='Sale Type', y='RMSE',
                             title='RMSE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'Tweedie':
            with cols[i]:
                df = pd.DataFrame({
                    'Sale Type': ['Big Sales', 'Low Sales'],
                    'Tweedie': tweedie
                })
                fig = px.bar(df, x='Sale Type', y='Tweedie',
                             title='Tweedie error',
                             height=300, width=250)
                st.write(fig)

def show_categories_analysis(**kwargs):
    selected_metrics = kwargs['selected_metrics']
    mae = kwargs['mae']
    wmape = kwargs['wmape']
    rmse = kwargs['rmse']
    tweedie = kwargs['tweedie']

    cols = st.columns(4)
    for i, metric in enumerate(selected_metrics):
        if metric == 'MAE':
            with cols[i]:
                df = pd.DataFrame({
                    'Category': ['FOODS', 'HOBBIES', 'HOUSEHOLD'],
                    'MAE': mae
                })
                fig = px.bar(df, x='Category', y='MAE',
                             title='MAE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'WMAPE':
            with cols[i]:
                df = pd.DataFrame({
                    'Category': ['FOODS', 'HOBBIES', 'HOUSEHOLD'],
                    'WMAPE': wmape
                })
                fig = px.bar(df, x='Category', y='WMAPE',
                             title='WMAPE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'RMSE':
            with cols[i]:
                df = pd.DataFrame({
                    'Category': ['FOODS', 'HOBBIES', 'HOUSEHOLD'],
                    'RMSE': rmse
                })
                fig = px.bar(df, x='Category', y='RMSE',
                             title='RMSE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'Tweedie':
            with cols[i]:
                df = pd.DataFrame({
                    'Category': ['FOODS', 'HOBBIES', 'HOUSEHOLD'],
                    'Tweedie': tweedie
                })
                fig = px.bar(df, x='Category', y='Tweedie',
                             title='Tweedie error',
                             height=300, width=250)
                st.write(fig)

def show_states_analysis(**kwargs):
    selected_metrics = kwargs['selected_metrics']
    mae = kwargs['mae']
    wmape = kwargs['wmape']
    rmse = kwargs['rmse']
    tweedie = kwargs['tweedie']

    cols = st.columns(4)
    for i, metric in enumerate(selected_metrics):
        if metric == 'MAE':
            with cols[i]:
                df = pd.DataFrame({
                    'State': ['CA', 'TX', 'WI'],
                    'MAE': mae
                })
                fig = px.bar(df, x='State', y='MAE',
                             title='MAE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'WMAPE':
            with cols[i]:
                df = pd.DataFrame({
                    'State': ['CA', 'TX', 'WI'],
                    'WMAPE': wmape
                })
                fig = px.bar(df, x='State', y='WMAPE',
                             title='WMAPE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'RMSE':
            with cols[i]:
                df = pd.DataFrame({
                    'State': ['CA', 'TX', 'WI'],
                    'RMSE': rmse
                })
                fig = px.bar(df, x='State', y='RMSE',
                             title='RMSE error',
                             height=300, width=250)
                st.write(fig)
        if metric == 'Tweedie':
            with cols[i]:
                df = pd.DataFrame({
                    'State': ['CA', 'TX', 'WI'],
                    'Tweedie': tweedie
                })
                fig = px.bar(df, x='State', y='Tweedie',
                             title='Tweedie error',
                             height=300, width=250)
                st.write(fig)
