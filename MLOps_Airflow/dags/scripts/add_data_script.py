import pickle

import numpy as np
import pandas as pd

from datetime import datetime, timedelta


def generate_data(data_batch_path, events_dict_path, snaps_dict_path):
    """
    Generates new rows of data according to the last day batch of data. This function has the role of simulating
    the entrance of new real data to be more faithful to a real situation. The new rows of data are not real, since the
    values of some columns are randomly obtained between a range of numbers. It has been done in a justified and logical
    way.

    Parameters
    ----------
    data_batch_path: Path where the new data batch is saved. (str)
    events_dict_path: Path where the events of a year are saved. (str)
    snaps_dict_path: Path where the snaps of a year are saved. (str)

    Returns
    -------
    new_data: New generated batch of data. (DataFrame)
    """
    data_batch = pd.read_csv(data_batch_path)

    # Modifying the column 'd'
    old_d = data_batch['d'].unique()[0]
    new_data = data_batch.assign(d='d_' + str(int(old_d[2:]) + 1))

    # Modifying the column 'sales'
    prob = (new_data.groupby('sales')['sales'].count() / len(new_data)).values
    x = sorted(new_data['sales'].unique())
    new_data = new_data.assign(sales=np.random.choice(x, p=prob, size=len(new_data)))

    # Modifying the column 'date'
    old_date = datetime.strptime(new_data['date'].unique()[0], "%Y-%m-%d")
    new_data = new_data.assign(date=datetime.strftime(old_date + timedelta(days=1), "%Y-%m-%d"))

    # Modifying the column 'wm_yr_wk'
    old_wm = new_data['wm_yr_wk'].unique()[0]
    old_wday = new_data['wday'].unique()[0]
    if old_wday == 7:
        new_data = new_data.assign(wm_yr_wk=old_wm + 1)
    else:
        new_data = new_data

    # Modifying the column 'wday'
    if old_wday == 7:
        new_data = new_data.assign(wday=1)
    else:
        new_data = new_data.assign(wday=old_wday + 1)

    # Modifying the column 'weekday'
    wday = new_data['wday'].unique()[0]
    if wday == 1:
        new_data = new_data.assign(weekday='Saturday')
    elif wday == 2:
        new_data = new_data.assign(weekday='Sunday')
    elif wday == 3:
        new_data = new_data.assign(weekday='Monday')
    elif wday == 4:
        new_data = new_data.assign(weekday='Tuesday')
    elif wday == 5:
        new_data = new_data.assign(weekday='Wednesday')
    elif wday == 6:
        new_data = new_data.assign(weekday='Thursday')
    else:
        new_data = new_data.assign(weekday='Friday')

    # Modifying the column 'month'
    new_data = new_data.assign(month=int(new_data['date'].unique()[0][5:7]))

    # Modifying the column 'year'
    new_data = new_data.assign(year=int(new_data['date'].unique()[0][:4]))

    # Modifying the 'event' columns
    new_data = new_events(new_data, events_dict_path)

    # Modifying the 'snap' columns
    new_data = new_snaps(new_data, snaps_dict_path)

    # Modifying the 'sell_price' column
    prices = new_data['sell_price'].values.tolist()
    if wday == 1:
        for i in range(0, len(prices)):
            random_numb = round(np.random.uniform(-0.1, 0.1), 2)
            prices[i] = round(prices[i] + random_numb, 2)
        new_data = new_data.assign(sell_price=prices)

    return new_data


def new_events(new_data, events_dict_path):
    """
    Function used within the generate_data function in order to complete certain columns, specifically those related to
    the events of the year. The function consists of consulting the dictionary of events of a calendar year, and
    assigning the corresponding event to the corresponding day of the new batch of data.

    Parameters
    ----------
    new_data: New generated batch of data. (DataFrame)
    events_dict_path: Path where the events of a year are saved. (str)

    Returns
    -------
    new_data: Updated new generated batch of data. (DataFrame)
    """
    with open(events_dict_path, 'rb') as f:
        year_events_dict = pickle.load(f)

    for dict_date in year_events_dict:
        if dict_date[5:] == new_data['date'].unique()[0][5:]:
            events_day = year_events_dict[dict_date]
        else:
            events_day = [np.nan, np.nan, np.nan, np.nan]

    new_data = new_data.assign(event_name_1=events_day[0],
                               event_type_1=events_day[1],
                               event_name_2=events_day[2],
                               event_type_2=events_day[3])
    return new_data


def new_snaps(new_data, snaps_dict_path):
    """
    Function used within the generate_data function in order to complete certain columns, specifically those related to
    the snaps of the year. The snap attributes indicate whether the stores allow purchases with snap food stamps on
    that day. The function consists of consulting the dictionary of snaps of a calendar year, and assigning the
    corresponding value to the corresponding day of the new batch of data.

    Parameters
    ----------
    new_data: New generated batch of data. (DataFrame)
    snaps_dict_path: Path where the snaps of a year are saved. (str)

    Returns
    -------
    new_data: Updated new generated batch of data. (DataFrame)
    """
    with open(snaps_dict_path, 'rb') as f:
        year_snaps_dict = pickle.load(f)

    for dict_date in year_snaps_dict:
        if dict_date[5:] == new_data['date'].unique()[0][5:]:
            snaps_day = year_snaps_dict[dict_date]
        else:
            snaps_day = [0, 0, 0]

    new_data = new_data.assign(snap_CA=snaps_day[0],
                               snap_TX=snaps_day[1],
                               snap_WI=snaps_day[2])
    return new_data
