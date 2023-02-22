import yaml
import logging
import scripts.custom_metrics as custom_metrics
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

with open('save_volume/config.yaml') as f:
     data = yaml.load(f, Loader=yaml.FullLoader)
     dates = data['dates']
     regression_data = data['regression']
     classification_data = data['classification']
     tasks = data['task']
     fname = data['filename']


def clas_decision_metric(decision_metric):
     match decision_metric:
         case 'accuracy':
             loss = accuracy_score
             score = 'accuracy'
         case 'precision':
             loss = precision_score
             score = 'precision'
         case 'recall':
             loss = recall_score
             score = 'recall'
         case 'f1':
             loss = f1_score
             score = 'f1'
     return loss, score


def reg_decision_metric(decision_metric):
     match decision_metric:
         case 'mae':
             loss = custom_metrics.mae_loss
             score = make_scorer(custom_metrics.mae_loss, greater_is_better=False)
         case 'wmape':
             loss = custom_metrics.wmape_loss
             score = make_scorer(custom_metrics.wmape_loss, greater_is_better=False)
         case 'rmse':
             loss = custom_metrics.rmse_loss
             score = make_scorer(custom_metrics.rmse_loss, greater_is_better=False)
         case 'tweedie':
             loss = custom_metrics.tweedie_loss
             score = make_scorer(custom_metrics.tweedie_loss, greater_is_better=False)
     return loss, score


def reg_global_analysis(predictions, true):
     logging.info('Computing errors for GLOBAL analysis.')
     results = {}
     for metric in regression_data['analysis_metrics']:
         match metric:
             case 'mae':
                 result = round(custom_metrics.mae_loss(predictions, true), 3)
                 results[metric] = result
             case 'wmape':
                 result = round(custom_metrics.wmape_loss(predictions, true), 3)
                 results[metric] = result
             case 'rmse':
                 result = round(custom_metrics.rmse_loss(predictions, true), 3)
                 results[metric] = result
             case 'tweedie':
                 result = round(custom_metrics.tweedie_loss(predictions, true), 3)
                 results[metric] = result
     print(results)


def reg_sales_analysis(predictions, true, big_sales=10):
     logging.info('Computing errors for SALES analysis.')
     true = true.reset_index(drop=True)
     true_big_sales = true[true > big_sales]
     true_low_sales = true[true <= big_sales]
     true_values = [true_big_sales, true_low_sales]
     mae, wmape, rmse, tweedie = ([], [], [], [])

     results = {}
     for true in true_values:
         indexes = true.index
         sales_predictions = [predictions[i] for i in indexes]

         for metric in regression_data['analysis_metrics']:
             match metric:
                 case 'mae':
                     sales_mae = round(custom_metrics.mae_loss(sales_predictions, true), 3)
                     mae.append(sales_mae)
                     results[metric] = mae
                 case 'wmape':
                     sales_wmape = round(custom_metrics.wmape_loss(sales_predictions, true), 3)
                     wmape.append(sales_wmape)
                     results[metric] = wmape
                 case 'rmse':
                     sales_rmse = round(custom_metrics.rmse_loss(sales_predictions, true), 3)
                     rmse.append(sales_rmse)
                     results[metric] = rmse
                 case 'tweedie':
                     sales_tweedie = round(custom_metrics.tweedie_loss(sales_predictions, true), 3)
                     tweedie.append(sales_tweedie)
                     results[metric] = tweedie

     print('The errors are displayed in the following way: [Big Sales, Low Sales]')
     print(results)


def reg_categories_analysis(predictions, true, data):
     logging.info('Computing errors for CATEGORIES analysis.')
     data = data.reset_index(drop=True)
     categories = ['cat_id_FOODS', 'cat_id_HOBBIES', 'cat_id_HOUSEHOLD']
     mae, wmape, rmse, tweedie = ([], [], [], [])

     results = {}
     for cat in categories:
         index = data[data[cat] == 1].index
         cat_true = true.iloc[index]
         cat_predictions = [predictions[i] for i in index]

         for metric in regression_data['analysis_metrics']:
             match metric:
                 case 'mae':
                     cat_mae = round(custom_metrics.mae_loss(cat_predictions, cat_true), 3)
                     mae.append(cat_mae)
                     results[metric] = mae
                 case 'wmape':
                     cat_wmape = round(custom_metrics.wmape_loss(cat_predictions, cat_true), 3)
                     wmape.append(cat_wmape)
                     results[metric] = wmape
                 case 'rmse':
                     cat_rmse = round(custom_metrics.rmse_loss(cat_predictions, cat_true), 3)
                     rmse.append(cat_rmse)
                     results[metric] = rmse
                 case 'tweedie':
                     cat_tweedie = round(custom_metrics.tweedie_loss(cat_predictions, cat_true), 3)
                     tweedie.append(cat_tweedie)
                     results[metric] = tweedie

     print('The errors are displayed in the following way: [FOOD, HOBBIES, HOUSEHOLD]')
     print(results)


def reg_states_analysis(predictions, true, data):
     logging.info('Computing errors for STATES analysis.')
     data = data.reset_index(drop=True)
     states = ['state_id_CA', 'state_id_TX', 'state_id_WI']
     mae, wmape, rmse, tweedie = ([], [], [], [])

     results = {}
     for sta in states:
         index = data[data[sta] == 1].index
         sta_true = true.iloc[index]
         sta_predictions = [predictions[i] for i in index]

         for metric in regression_data['analysis_metrics']:
             match metric:
                 case 'mae':
                     sta_mae = round(custom_metrics.mae_loss(sta_predictions, sta_true), 3)
                     mae.append(sta_mae)
                     results[metric] = mae
                 case 'wmape':
                     sta_wmape = round(custom_metrics.wmape_loss(sta_predictions, sta_true), 3)
                     wmape.append(sta_wmape)
                     results[metric] = wmape
                 case 'rmse':
                     sta_rmse = round(custom_metrics.rmse_loss(sta_predictions, sta_true), 3)
                     rmse.append(sta_rmse)
                     results[metric] = rmse
                 case 'tweedie':
                     sta_tweedie = round(custom_metrics.tweedie_loss(sta_predictions, sta_true), 3)
                     tweedie.append(sta_tweedie)
                     results[metric] = tweedie

     print('The errors are displayed in the following way: [CA, TX, WI]')
     print(results)


def clas_global_analysis(predictions, true):
     logging.info('Computing errors for GLOBAL analysis.')
     results = {}
     for metric in classification_data['analysis_metrics']:
         match metric:
             case 'accuracy':
                 result = round(accuracy_score(predictions, true), 3)
                 results[metric] = result
             case 'precision':
                 result = round(precision_score(predictions, true, pos_label='Incrementa'), 3)
                 results[metric] = result
             case 'recall':
                 result = round(recall_score(predictions, true, pos_label='Incrementa'), 3)
                 results[metric] = result
             case 'tweedie':
                 result = round(f1_score(predictions, true, pos_label='Incrementa'), 3)
                 results[metric] = result
     print(results)


def clas_categories_analysis(predictions, true, data):
     logging.info('Computing errors for CATEGORIES analysis.')
     data = data.reset_index(drop=True)
     categories = ['cat_id_FOODS', 'cat_id_HOBBIES', 'cat_id_HOUSEHOLD']
     accuracy, precision, recall, f1 = ([], [], [], [])

     results = {}
     for cat in categories:
         index = data[data[cat] == 1].index
         cat_true = true.iloc[index]
         cat_predictions = [predictions[i] for i in index]

         for metric in classification_data['analysis_metrics']:
             match metric:
                 case 'accuracy':
                     cat_accuracy = round(accuracy_score(cat_predictions, cat_true), 3)
                     accuracy.append(cat_accuracy)
                     results[metric] = accuracy
                 case 'precision':
                     cat_precision = round(precision_score(cat_predictions, cat_true, pos_label='Incrementa'), 3)
                     precision.append(cat_precision)
                     results[metric] = precision
                 case 'recall':
                     cat_recall = round(recall_score(cat_predictions, cat_true, pos_label='Incrementa'), 3)
                     recall.append(cat_recall)
                     results[metric] = recall
                 case 'tweedie':
                     cat_f1 = round(f1_score(cat_predictions, cat_true, pos_label='Incrementa'), 3)
                     f1.append(cat_f1)
                     results[metric] = f1

     print('The errors are displayed in the following way: [FOOD, HOBBIES, HOUSEHOLD]')
     print(results)


def clas_states_analysis(predictions, true, data):
     logging.info('Computing errors for STATES analysis.')
     data = data.reset_index(drop=True)
     states = ['state_id_CA', 'state_id_TX', 'state_id_WI']
     accuracy, precision, recall, f1 = ([], [], [], [])

     results = {}
     for sta in states:
         index = data[data[sta] == 1].index
         sta_true = true.iloc[index]
         sta_predictions = [predictions[i] for i in index]

         for metric in classification_data['analysis_metrics']:
             match metric:
                 case 'accuracy':
                     sta_accuracy = round(accuracy_score(sta_predictions, sta_true), 3)
                     accuracy.append(sta_accuracy)
                     results[metric] = accuracy
                 case 'precision':
                     sta_precision = round(precision_score(sta_predictions, sta_true, pos_label='Incrementa'), 3)
                     precision.append(sta_precision)
                     results[metric] = precision
                 case 'recall':
                     sta_recall = round(recall_score(sta_predictions, sta_true, pos_label='Incrementa'), 3)
                     recall.append(sta_recall)
                     results[metric] = recall
                 case 'tweedie':
                     sta_f1 = round(f1_score(sta_predictions, sta_true, pos_label='Incrementa'), 3)
                     f1.append(sta_f1)
                     results[metric] = f1

     print('The errors are displayed in the following way: [CA, TX, WI]')
     print(results)
