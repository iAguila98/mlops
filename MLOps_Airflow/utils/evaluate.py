import custom_metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging

def reg_test(model, test_X, test_y):
    logging.info('Starting the test evaluation.')
    predictions = model.predict(test_X)
    mae = round(custom_metrics.mae_loss(predictions, test_y), 3)
    wmape = round(custom_metrics.wmape_loss(predictions, test_y), 3)
    rmse = round(custom_metrics.rmse_loss(predictions, test_y), 3)
    tweedie = round(custom_metrics.tweedie_loss(test_y, predictions), 3)
    print(f'mae = {mae}, wmape = {wmape}, rmse = {rmse}, tweedie = {tweedie}')
    return mae, wmape, rmse, tweedie

def clas_test(model, test_X, test_y):
    logging.info('Starting the test evaluation.')
    predictions = model.predict(test_X)
    accuracy = round(accuracy_score(predictions, test_y), 3)
    precision = round(precision_score(predictions, test_y,  pos_label='Incrementa'), 3)
    recall = round(recall_score(predictions, test_y,  pos_label='Incrementa'), 3)
    f1 = round(f1_score(test_y, predictions,  pos_label='Incrementa'), 3)
    print(f'accuracy = {accuracy}, precision = {precision}, recall = {recall}, f1 = {f1}')
    return accuracy, precision, recall, f1
