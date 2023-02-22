import numpy as np
from sklearn.metrics import mean_squared_error, mean_tweedie_deviance, mean_absolute_error


def mae_loss(predictions, true):
    return mean_absolute_error(predictions, true)


def wmape_loss(predictions, true):
    return np.mean(np.abs(true - predictions)) / np.mean(true)


def rmse_loss(predictions, true):
    return np.sqrt(mean_squared_error(predictions, true))


def tweedie_loss(predictions, true):
    return mean_tweedie_deviance(true, predictions)
