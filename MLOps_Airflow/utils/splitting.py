import scripts.utils as utils

def split_dataset(dataset):
    test_set = dataset[dataset['date'] >= utils.dates['test_date']]
    val_set = dataset[(dataset['date'] >= utils.dates['train_date']) & (dataset['date'] < utils.dates['val_date'])]
    training_set = dataset[dataset['date'] < utils.dates['train_date']]

    # We delete the target column, and we also delete 'date' column used for the split.
    if utils.tasks['classification']:
        test_X = test_set.drop(['classification', 'date'], axis=1)
        test_y = test_set['classification']
        val_X = val_set.drop(['classification', 'date'], axis=1)
        val_y = val_set['classification']
        train_X = training_set.drop(['classification', 'date'], axis=1)
        train_y = training_set['classification']
    else:
        test_X = test_set.drop(['sales', 'date'], axis=1)
        test_y = test_set['sales']
        val_X = val_set.drop(['sales', 'date'], axis=1)
        val_y = val_set['sales']
        train_X = training_set.drop(['sales', 'date'], axis=1)
        train_y = training_set['sales']

    return train_X, train_y, val_X, val_y, test_X, test_y
