import numpy as np
import pandas as pd

from category_encoders import TargetEncoder
from datetime import datetime, timedelta
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class FillSellPrice(BaseEstimator, TransformerMixin):
    """
    Fill sell_price Nan using backward fill without taking into account special event prices.
    Afterward, event days prices are filled using the mean of the product price.
    """
    def __init__(self):
        self.cat_attributes = ['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X[self.cat_attributes] = X[self.cat_attributes].fillna('NoEvent')
        no_events = X[X['event_name_1'] == 'NoEvent'].sort_values('date')
        X['sell_price'] = no_events.groupby('id')['sell_price'].bfill().sort_index()
        X['sell_price'] = X.groupby('id')['sell_price'].transform(lambda x: x.fillna(x.mean()))
        return X


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """
    This class applies OneHotEncoding (get_dummies) to a specific categorical attributes with low number of
    categories. After that, it combines the event type 1 and event type 2 columns that are common (Religious,
    Cultural and NoEvent). The National and Sporting type only exists in type_1, so they will be just renamed.
    NoEvent is the only one resulting from an AND logic, since both types should be NoEvent to have a 1 in
    the new column. For the rest of types, we use the OR logic.

    For the categorical attributes with a bigger number of categories, the class applies TargetEncoder.
    """

    def __init__(self):
        self.tr_enc = TargetEncoder()
        self.ohe_attr = ['cat_id', 'state_id', 'event_type_1', 'event_type_2']
        self.tr_attr = ['event_name_1', 'event_name_2']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Convert item_id strings into numbers by using factorize function
        X['item_id'] = pd.factorize(X['item_id'])[0]

        # We group snaps as the country id is enough to determine what state has snap
        X['snap'] = np.where((X['state_id'] == 'CA') & (X['snap_CA'] == 1) |
                             (X['state_id'] == 'TX') & (X['snap_TX'] == 1) |
                             (X['state_id'] == 'WI') & (X['snap_WI'] == 1), 1, 0)

        # Apply One Hot Encoding by using the get_dummies function
        X = pd.get_dummies(X, columns=self.ohe_attr)

        # Group the duplicated columns created by some of the categories of event_type features
        X['event_type_Religious'] = X.event_type_1_Religious | X.event_type_2_Religious
        X['event_type_Cultural'] = X.event_type_1_Cultural | X.event_type_2_Cultural
        X['event_type_NoEvent'] = X.event_type_1_NoEvent & X.event_type_2_NoEvent

        X = X.rename(columns={'event_type_1_Sporting': 'event_type_Sporting',
                              'event_type_1_National': 'event_type_National'})

        X = X.drop(columns=['event_type_1_Religious', 'event_type_2_Religious',
                            'event_type_1_Cultural', 'event_type_2_Cultural',
                            'event_type_1_NoEvent', 'event_type_2_NoEvent',
                            'snap_CA', 'snap_TX', 'snap_WI'])

        # Take the date from 28 days ago, the models will try to forecast those 28 days.
        last_day = X['date'].iat[-1]
        last_day = datetime.strptime(last_day, "%Y-%m-%d")
        forecast_date = last_day - timedelta(days=28)
        forecast_date = datetime.strftime(forecast_date, "%Y-%m-%d")

        # Apply Target Encoding. The training set will only have information in its dates. The same for the test set.
        transformed_train = self.tr_enc.fit_transform(X[X['date'] < forecast_date][self.tr_attr],
                                                      X[X['date'] < forecast_date]['sales'],
                                                      smoothing=1.0)
        transformed_test = self.tr_enc.fit_transform(X[X['date'] >= forecast_date][self.tr_attr],
                                                     X[X['date'] >= forecast_date]['sales'],
                                                     smoothing=1.0)

        # Concat train and test set again after the target encoding
        transformed_data = pd.concat([transformed_train, transformed_test], ignore_index=True)

        # Delete the columns that are obsolete after applying the target encoding to them
        X = X.drop(columns=self.tr_attr)
        X = pd.concat([X, transformed_data], axis=1)

        return X


class AddLag(BaseEstimator, TransformerMixin):
    """
    Class that adds new lag features on the sales number according to each product. It also adds features indicating
    the mean sales over the last x days. Finally, it is decided to create a new binary feature in the dataset that
    indicates whether it is a weekend or not.

    """

    def __init__(self, lags=(5, 10, 15, 20, 28),
                 add_weekend=True,
                 add_mean_lag=True,
                 means=(7, 14)):
        self.lags = lags
        self.add_weekend = add_weekend
        self.add_mean_lag = add_mean_lag
        self.means = means

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for lag in self.lags:
            X['lag_' + str(lag)] = X.groupby('id')['sales'].shift(lag)

        if self.add_weekend:
            X['weekend'] = np.where((X['wday'] == 7) | (X['wday'] == 1) | (X['wday'] == 2), 1, 0)

        if self.add_mean_lag:
            for mns in self.means:
                X['mean_' + str(mns)] = X.groupby('id')['sales'].transform(
                    lambda x: x.rolling(mns).mean())

        return X


class DeleteFeatures(BaseEstimator, TransformerMixin):
    """
    This class deletes the attributes indicated by the user.
    """

    def __init__(self, attributes):
        self.attributes = attributes

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X[X.columns[~X.columns.isin(self.attributes)]]
        return X


class DropNa(BaseEstimator, TransformerMixin):
    """
    This class performs a drop of all rows with any NaN values that remains in the dataset.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.dropna(axis=0, how='any', inplace=True)

        return X


def preprocessing_pipeline(dataset):
    """
    This function builds the preprocessing pipeline with the previous classes.
    """
    del_attr = ['id', 'dept_id', 'store_id', 'd', 'wm_yr_wk', 'weekday', 'year']

    pipeline = Pipeline([
        ('fill_price', FillSellPrice()),
        ('cat_encoder', CategoricalEncoder()),
        ('add_lag', AddLag()),
        ('delete_features', DeleteFeatures(attributes=del_attr)),
        ('drop_na', DropNa())
    ])

    prepared_set = pipeline.fit_transform(dataset)
    return prepared_set
