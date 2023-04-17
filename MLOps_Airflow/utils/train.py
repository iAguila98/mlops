import pandas as pd
import logging
import scripts.error_analysis as error_analysis
import scripts.evaluate as evaluate
import pickle
import scripts.utils as utils
from scripts.training_regressor import TrainRegressor
from scripts.training_classifier import TrainClassifier

logging.basicConfig(level=logging.INFO)
logging.info('The execution has started.')


def main():

    if utils.tasks['classification']:
        path = 'save_volume/preprocessed_data_cls.csv'
        logging.info('Reading the dataset.')
        dataset = pd.read_csv(path, index_col=0)

        logging.info('Classification task has started.')
        train_classifier = TrainClassifier(dataset)

        logging.info('Splitting the dataset.')
        train_X, train_y, val_X, val_y, test_X, test_y = train_classifier.splitting()

        model = train_classifier.select_model(train_X=train_X, train_y=train_y, val_X=val_X, val_y=val_y)
        train_classifier.error_analysis(model=model, val_X=val_X, val_y=val_y)
        train_classifier.evaluate(model=model, test_X=test_X, test_y=test_y)

    else:
        path = 'save_volume/old_preprocessed_data.csv'
        logging.info('Reading the dataset.')
        dataset = pd.read_csv(path, index_col=0)

        logging.info('Regression task has started.')
        train_regressor = TrainRegressor(dataset)

        logging.info('Splitting the dataset.')
        train_X, train_y, val_X, val_y, test_X, test_y = train_regressor.splitting()

        model = train_regressor.select_model(train_X=train_X, train_y=train_y, val_X=val_X, val_y=val_y)
        train_regressor.error_analysis(model=model, val_X=val_X, val_y=val_y)
        train_regressor.evaluate(model=model, test_X=test_X, test_y=test_y)

    pickle.dump(model, open('save_volume/models/' + utils.fname, 'wb'))


if __name__ == '__main__':
    main()
