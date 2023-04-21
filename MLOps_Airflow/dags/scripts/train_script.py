import pandas as pd


def train(model, train_path):
    """


    Parameters
    ----------
    model
    train_path

    Returns
    -------
    """
    df = pd.read_csv(train_path)
    target_col = 'sales'
    train_x = df.drop([target_col, 'date'], axis='columns')
    train_y = df[target_col]

    trained_model = model.fit(train_x, train_y)
    train_date = pd.to_datetime('now', utc=True)

    return trained_model, train_date