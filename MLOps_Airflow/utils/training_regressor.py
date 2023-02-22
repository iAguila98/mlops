from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import scripts.custom_metrics as custom_metrics
import logging
import scripts.utils as utils


class TrainRegressor():
    def __init__(self, dataset):
        self.dataset = dataset
        self.algorithms = utils.regression_data['algorithms']
        self.decision_metric = utils.regression_data['decision_metric']

    def splitting(self):
        test_set = self.dataset[self.dataset['date'] >= utils.dates['test_date']]
        val_set = self.dataset[(self.dataset['date'] >= utils.dates['train_date'])
                               & (self.dataset['date'] < utils.dates['val_date'])]
        training_set = self.dataset[self.dataset['date'] < utils.dates['train_date']]

        test_X = test_set.drop(['sales', 'date'], axis=1)
        test_y = test_set['sales']
        val_X = val_set.drop(['sales', 'date'], axis=1)
        val_y = val_set['sales']
        train_X = training_set.drop(['sales', 'date'], axis=1)
        train_y = training_set['sales']

        return train_X, train_y, val_X, val_y, test_X, test_y

    def select_model(self, **kwargs):
        """
            Function used to train different regression models to predict sales. It also selects the best one depending
            on the decision_metric indicated in the YAML file. The ML models tried are also selected in the YAML file
            along with their correspondent hyperparameters. The model will be trained with GridSearch if it is indicated
            in the YAML. GridSearch will be applied with the decision_metric selected.

            Inputs:
                val_X, val_y: Validation data and labels
                train_X, train_y: Training data and labels

            Output:
                best_model: Model with the minimum error indicated by the decision_metric.
                predictions: Predictions of the validation set made by the model.
        """
        loss, score = utils.reg_decision_metric(self.decision_metric)
        errors = {}
        if 'linear_regression' in self.algorithms.keys():
            logging.info('Training linear model...')
            regressor = LinearRegression()
            if self.algorithms['linear_regression']:
                grid_search = GridSearchCV(regressor,
                                           utils.regression_data['linear_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_linear_model = grid_search.best_estimator_
                predictions = best_linear_model.predict(kwargs['val_X'])
                errors[best_linear_model] = loss(predictions, kwargs['val_y'])

            else:
                regressor.fit(kwargs['train_X'], kwargs['train_y'])
                best_linear_model = regressor
                predictions = best_linear_model.predict(kwargs['val_X'])
                errors[best_linear_model] = loss(predictions, kwargs['val_y'])

        if 'decision_tree' in self.algorithms.keys():
            logging.info('Training decision tree model...')
            regressor = DecisionTreeRegressor()
            if self.algorithms['decision_tree']:
                grid_search = GridSearchCV(regressor,
                                           utils.regression_data['decision_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_tree_model = grid_search.best_estimator_
                predictions = best_tree_model.predict(kwargs['val_X'])
                errors[best_tree_model] = loss(predictions, kwargs['val_y'])

            else:
                regressor.fit(kwargs['train_X'], kwargs['train_y'])
                best_tree_model = regressor
                predictions = best_tree_model.predict(kwargs['val_X'])
                errors[best_tree_model] = loss(predictions, kwargs['val_y'])

        if 'random_forest' in self.algorithms.keys():
            logging.info('Training random forest model...')
            regressor = RandomForestRegressor()
            if self.algorithms['random_forest']:
                grid_search = GridSearchCV(regressor,
                                           utils.regression_data['forest_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_forest_model = grid_search.best_estimator_
                predictions = best_forest_model.predict(kwargs['val_X'])
                errors[best_forest_model] = loss(predictions, kwargs['val_y'])

            else:
                regressor.fit(kwargs['train_X'], kwargs['train_y'])
                best_forest_model = regressor
                predictions = best_forest_model.predict(kwargs['val_X'])
                errors[best_forest_model] = loss(predictions, kwargs['val_y'])

        logging.info(errors)

        return min(errors, key=errors.get)

    def error_analysis(self, **kwargs):
        """
            Function used to obtain the error values depending on what we desire to analyse. For example, we can observe
            the errors for big and low quantities of sales, for the different categories, etc. These errors are
            computed with different metrics that the user can select in the YAML file (analysis_metrics).

            Inputs:
                model: Trained model that we want to analize
                val_X, val_y: Validation data and labels.

        """
        predictions = kwargs['model'].predict(kwargs['val_X'])

        if 'global' in utils.regression_data['analysis']:
            utils.reg_global_analysis(predictions, kwargs['val_y'])

        if 'sales' in utils.regression_data['analysis']:
            utils.reg_sales_analysis(predictions, kwargs['val_y'], 10)

        if 'categories' in utils.regression_data['analysis']:
            utils.reg_categories_analysis(predictions, kwargs['val_y'], kwargs['val_X'])

        if 'states' in utils.regression_data['analysis']:
            utils.reg_states_analysis(predictions, kwargs['val_y'], kwargs['val_X'])


    def evaluate(self, **kwargs):
        logging.info('Starting the test evaluation.')
        predictions = kwargs['model'].predict(kwargs['test_X'])

        mae = round(custom_metrics.mae_loss(predictions, kwargs['test_y']), 3)
        wmape = round(custom_metrics.wmape_loss(predictions, kwargs['test_y']), 3)
        rmse = round(custom_metrics.rmse_loss(predictions, kwargs['test_y']), 3)
        tweedie = round(custom_metrics.tweedie_loss(kwargs['test_y'], predictions), 3)

        print(f'mae = {mae}, wmape = {wmape}, rmse = {rmse}, tweedie = {tweedie}')