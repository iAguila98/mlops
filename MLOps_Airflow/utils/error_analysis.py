import logging
import scripts.custom_metrics as custom_metrics
import scripts.utils as utils
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def compute_reg_errors(model, val_X, val_y):
    """
        Function used to obtain the error values depending on what we desire to analyse. For example, we can observe
        the errors for big and low quantities of sales, for the different categories, etc.
        Inputs:
            analyze: Argument that indicates which kind of error analysis we desire.
            model: Trained model that we want to analize
            predictions: Predictions of the validation set made by the model.
            val_X, val_y: Validation data and labels.

        Output:
            mae, wmape, rmse, tweedie: Values of the mae, wmape, rmse and tweedie errors

    """
    predictions = model.predict(val_X)

    if 'global' in utils.regression_data['analysis']:
        logging.info('Computing errors for GLOBAL analysis.')
        results = {}
        for metric in utils.regression_data['analysis_metrics']:
            if metric == 'mae':
                result = round(custom_metrics.mae_loss(predictions, val_y), 3)
                results[metric] = result
            elif metric == 'wmape':
                result = round(custom_metrics.wmape_loss(predictions, val_y), 3)
                results[metric] = result
            elif metric == 'rmse':
                result = round(custom_metrics.rmse_loss(predictions, val_y), 3)
                results[metric] = result
            else:
                result = round(custom_metrics.tweedie_loss(predictions, val_y), 3)
                results[metric] = result
        print(results)

    if 'sales' in utils.regression_data['analysis']:
        logging.info('Computing errors for SALES analysis.')

        val_y = val_y.reset_index(drop=True)
        threshold = 10
        true_big_sales = val_y[val_y > threshold]
        true_low_sales = val_y[val_y <= threshold]
        true_values = [true_big_sales, true_low_sales]
        mae, wmape, rmse, tweedie = ([], [], [], [])

        results = {}
        for true in true_values:
            indexes = true.index
            sales_predictions = [predictions[i] for i in indexes]

            for metric in utils.regression_data['analysis_metrics']:
                if metric == 'mae':
                    sales_mae = round(custom_metrics.mae_loss(sales_predictions, true), 3)
                    mae.append(sales_mae)
                    results[metric] = mae
                elif metric == 'wmape':
                    sales_wmape = round(custom_metrics.wmape_loss(sales_predictions, true), 3)
                    wmape.append(sales_wmape)
                    results[metric] = wmape
                elif metric == 'rmse':
                    sales_rmse = round(custom_metrics.rmse_loss(sales_predictions, true), 3)
                    rmse.append(sales_rmse)
                    results[metric] = rmse
                else:
                    sales_tweedie = round(custom_metrics.tweedie_loss(sales_predictions, true), 3)
                    tweedie.append(sales_tweedie)
                    results[metric] = tweedie

        print('The errors are displayed in the following way: [Big Sales, Low Sales]')
        print(results)

    results = {}
    if 'categories' in utils.regression_data['analysis']:
        logging.info('Computing errors for CATEGORIES analysis.')

        val_X = val_X.reset_index(drop=True)
        categories = ['cat_id_FOODS', 'cat_id_HOBBIES', 'cat_id_HOUSEHOLD']
        mae, wmape, rmse, tweedie = ([], [], [], [])

        for cat in categories:
            index = val_X[val_X[cat] == 1].index
            cat_true = val_y.iloc[index]
            cat_predictions = [predictions[i] for i in index]

            for metric in utils.regression_data['analysis_metrics']:
                if metric == 'mae':
                    cat_mae = round(custom_metrics.mae_loss(cat_predictions, cat_true), 3)
                    mae.append(cat_mae)
                    results[metric] = mae
                elif metric == 'wmape':
                    cat_wmape = round(custom_metrics.wmape_loss(cat_predictions, cat_true), 3)
                    wmape.append(cat_wmape)
                    results[metric] = wmape
                elif metric == 'rmse':
                    cat_rmse = round(custom_metrics.rmse_loss(cat_predictions, cat_true), 3)
                    rmse.append(cat_rmse)
                    results[metric] = rmse
                else:
                    cat_tweedie = round(custom_metrics.tweedie_loss(cat_predictions, cat_true), 3)
                    tweedie.append(cat_tweedie)
                    results[metric] = tweedie

        print('The errors are displayed in the following way: [FOOD, HOBBIES, HOUSEHOLD]')
        print(results)

    if 'states' in utils.regression_data['analysis']:
        logging.info('Computing errors for STATES analysis.')

        val_X = val_X.reset_index(drop=True)

        states = ['state_id_CA', 'state_id_TX', 'state_id_WI']
        mae, wmape, rmse, tweedie = ([], [], [], [])

        results = {}
        for sta in states:
            index = val_X[val_X[sta] == 1].index
            sta_true = val_y.iloc[index]
            sta_predictions = [predictions[i] for i in index]

            for metric in utils.regression_data['analysis_metrics']:
                if metric == 'mae':
                    sta_mae = round(custom_metrics.mae_loss(sta_predictions, sta_true), 3)
                    mae.append(sta_mae)
                    results[metric] = mae
                elif metric == 'wmape':
                    sta_wmape = round(custom_metrics.wmape_loss(sta_predictions, sta_true), 3)
                    wmape.append(sta_wmape)
                    results[metric] = wmape
                elif metric == 'rmse':
                    sta_rmse = round(custom_metrics.rmse_loss(sta_predictions, sta_true), 3)
                    rmse.append(sta_rmse)
                    results[metric] = rmse
                else:
                    sta_tweedie = round(custom_metrics.tweedie_loss(sta_predictions, sta_true), 3)
                    tweedie.append(sta_tweedie)
                    results[metric] = tweedie

        print('The errors are displayed in the following way: [CA, TX, WI]')
        print(results)


def compute_clas_errors(model, val_X, val_y):
    """
        Function used to obtain the error values depending on what we desire to analyse. For example, we can observe
        the errors for big and low quantities of sales, for the different categories, etc.
        Inputs:
            analyze: Argument that indicates which kind of error analysis we desire.
            model: Trained model that we want to analize
            predictions: Predictions of the validation set made by the model.
            val_X, val_y: Validation data and labels.

        Output:
            mae, wmape, rmse, tweedie: Values of the mae, wmape, rmse and tweedie errors

    """
    predictions = model.predict(val_X)

    if 'global' in utils.classification_data['analysis']:
        logging.info('Computing errors for GLOBAL analysis.')
        results = {}
        for metric in utils.classification_data['analysis_metrics']:
            if metric == 'accuracy':
                result = round(accuracy_score(predictions, val_y), 3)
                results[metric] = result
            elif metric == 'precision':
                result = round(precision_score(predictions, val_y,  pos_label='Incrementa'), 3)
                results[metric] = result
            elif metric == 'recall':
                result = round(recall_score(predictions, val_y,  pos_label='Incrementa'), 3)
                results[metric] = result
            else:
                result = round(f1_score(predictions, val_y,  pos_label='Incrementa'), 3)
                results[metric] = result
        print(results)

    results = {}
    if 'categories' in utils.classification_data['analysis']:
        logging.info('Computing errors for CATEGORIES analysis.')

        val_X = val_X.reset_index(drop=True)
        categories = ['cat_id_FOODS', 'cat_id_HOBBIES', 'cat_id_HOUSEHOLD']
        accuracy, precision, recall, f1 = ([], [], [], [])

        for cat in categories:
            index = val_X[val_X[cat] == 1].index
            cat_true = val_y.iloc[index]
            cat_predictions = [predictions[i] for i in index]

            for metric in utils.classification_data['analysis_metrics']:
                if metric == 'accuracy':
                    cat_accuracy = round(accuracy_score(cat_predictions, cat_true), 3)
                    accuracy.append(cat_accuracy)
                    results[metric] = accuracy
                elif metric == 'precision':
                    cat_precision = round(precision_score(cat_predictions, cat_true,  pos_label='Incrementa'), 3)
                    precision.append(cat_precision)
                    results[metric] = precision
                elif metric == 'recall':
                    cat_recall = round(recall_score(cat_predictions, cat_true,  pos_label='Incrementa'), 3)
                    recall.append(cat_recall)
                    results[metric] = recall
                else:
                    cat_f1 = round(f1_score(cat_predictions, cat_true,  pos_label='Incrementa'), 3)
                    f1.append(cat_f1)
                    results[metric] = f1

        print('The errors are displayed in the following way: [FOOD, HOBBIES, HOUSEHOLD]')
        print(results)

    if 'states' in utils.classification_data['analysis']:
        logging.info('Computing errors for STATES analysis.')

        val_X = val_X.reset_index(drop=True)

        states = ['state_id_CA', 'state_id_TX', 'state_id_WI']
        accuracy, precision, recall, f1 = ([], [], [], [])

        results = {}
        for sta in states:
            index = val_X[val_X[sta] == 1].index
            sta_true = val_y.iloc[index]
            sta_predictions = [predictions[i] for i in index]

            for metric in utils.classification_data['analysis_metrics']:
                if metric == 'accuracy':
                    sta_accuracy = round(accuracy_score(sta_predictions, sta_true), 3)
                    accuracy.append(sta_accuracy)
                    results[metric] = accuracy
                elif metric == 'precision':
                    sta_precision = round(precision_score(sta_predictions, sta_true,  pos_label='Incrementa'), 3)
                    precision.append(sta_precision)
                    results[metric] = precision
                elif metric == 'recall':
                    sta_recall = round(recall_score(sta_predictions, sta_true,  pos_label='Incrementa'), 3)
                    recall.append(sta_recall)
                    results[metric] = recall
                else:
                    sta_f1 = round(f1_score(sta_predictions, sta_true,  pos_label='Incrementa'), 3)
                    f1.append(sta_f1)
                    results[metric] = f1

        print('The errors are displayed in the following way: [CA, TX, WI]')
        print(results)
