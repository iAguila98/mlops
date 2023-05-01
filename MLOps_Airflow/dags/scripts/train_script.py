import pandas as pd


def train(model, train_path):
    """
    Train the model with the train set data. Before performing the .fit function, it splits the training set in order
    to separate the data from the target column. It also saves the date when the training has been performed, in order
    to save it as information in the historical dataset.

    Parameters
    ----------
    model: Model of scikit-learn to be trained.
    train_path: Path that indicates the training dataset. (str)

    Returns
    -------
    trained_model: Model trained with the test set.
    train_date: Date that indicates the moment of the training. (datetime)
    """
    # Read the train set and split it into train_x and train_y
    df = pd.read_csv(train_path)
    target_col = 'sales'
    train_x = df.drop([target_col, 'date'], axis='columns')
    train_y = df[target_col]

    # Train the model and save the date
    trained_model = model.fit(train_x, train_y)
    train_date = pd.to_datetime('now', utc=True)

    return trained_model, train_date
