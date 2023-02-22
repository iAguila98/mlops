from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
import scripts.utils as utils


class TrainClassifier():
    def __init__(self, dataset):
        self.dataset = dataset
        self.algorithms = utils.classification_data['algorithms']
        self.decision_metric = utils.classification_data['decision_metric']

    def splitting(self):
        test_set = self.dataset[self.dataset['date'] >= utils.dates['test_date']]
        val_set = self.dataset[(self.dataset['date'] >= utils.dates['train_date'])
                               & (self.dataset['date'] < utils.dates['val_date'])]
        training_set = self.dataset[self.dataset['date'] < utils.dates['train_date']]

        test_X = test_set.drop(['classification', 'date'], axis=1)
        test_y = test_set['classification']
        val_X = val_set.drop(['classification', 'date'], axis=1)
        val_y = val_set['classification']
        train_X = training_set.drop(['classification', 'date'], axis=1)
        train_y = training_set['classification']

        return train_X, train_y, val_X, val_y, test_X, test_y

    def select_model(self, **kwargs):
        """
            Function used to train different classifier models. It also selects the best one depending
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
        loss, score = utils.clas_decision_metric(self.decision_metric)
        errors = {}
        if 'sgd_classifier' in self.algorithms.keys():
            logging.info('Training sgd model...')
            classifier = SGDClassifier()
            if self.algorithms['sgd_classifier']:
                grid_search = GridSearchCV(classifier,
                                           utils.classification_data['sgd_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_linear_model = grid_search.best_estimator_
                predictions = best_linear_model.predict(kwargs['val_X'])
                errors[best_linear_model] = loss(kwargs['val_y'], predictions)

            else:
                classifier.fit(kwargs['train_X'], kwargs['train_y'])
                best_linear_model = classifier
                predictions = best_linear_model.predict(kwargs['val_X'])
                errors[best_linear_model] = loss(kwargs['val_y'], predictions)

        if 'decision_tree' in self.algorithms.keys():
            logging.info('Training decision tree model...')
            classifier = DecisionTreeClassifier()
            if self.algorithms['decision_tree']:
                grid_search = GridSearchCV(classifier,
                                           utils.classification_data['decision_class_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_tree_model = grid_search.best_estimator_
                predictions = best_tree_model.predict(kwargs['val_X'])
                errors[best_tree_model] = loss(kwargs['val_y'], predictions)

            else:
                classifier.fit(kwargs['train_X'], kwargs['train_y'])
                best_tree_model = classifier
                predictions = best_tree_model.predict(kwargs['val_X'])
                errors[best_tree_model] = loss(kwargs['val_y'], predictions)

        if 'random_forest' in self.algorithms().keys():
            logging.info('Training random forest model...')
            classifier = RandomForestClassifier()
            if self.algorithms['random_forest']:
                grid_search = GridSearchCV(classifier,
                                           utils.classification_data['forest_class_grid'],
                                           scoring=score
                                           )
                grid_search.fit(kwargs['train_X'], kwargs['train_y'])
                best_forest_model = grid_search.best_estimator_
                predictions = best_forest_model.predict(kwargs['val_X'])
                errors[best_forest_model] = loss(kwargs['val_y'], predictions)

            else:
                classifier.fit(kwargs['train_X'], kwargs['train_y'])
                best_forest_model = classifier
                predictions = best_forest_model.predict(kwargs['val_X'])
                errors[best_forest_model] = loss(kwargs['val_y'], predictions)

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

        if 'global' in utils.classification_data['analysis']:
            utils.clas_global_analysis(predictions, kwargs['val_y'])

        if 'categories' in utils.classification_data['analysis']:
            utils.clas_categories_analysis(predictions, kwargs['val_y'], kwargs['val_X'])

        if 'states' in utils.classification_data['analysis']:
            utils.clas_states_analysis(predictions, kwargs['val_y'], kwargs['val_X'])

    def evaluate(self, **kwargs):
        logging.info('Starting the test evaluation.')
        predictions = kwargs['model'].predict(kwargs['test_X'])

        accuracy = round(accuracy_score(predictions, kwargs['test_y']), 3)
        precision = round(precision_score(predictions, kwargs['test_y'], pos_label='Incrementa'), 3)
        recall = round(recall_score(predictions, kwargs['test_y'], pos_label='Incrementa'), 3)
        f1 = round(f1_score(kwargs['test_y'], predictions, pos_label='Incrementa'), 3)

        print(f'accuracy = {accuracy}, precision = {precision}, recall = {recall}, f1 = {f1}')