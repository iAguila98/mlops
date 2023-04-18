import pickle

import numpy as np
import pandas as pd

from datetime import datetime, timedelta

def generate_data(data_batch_path):
    """

    Parameters
    ----------
    data_batch_path

    Returns
    -------

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

    # Modifying the column 'wday'
    old_wday = new_data['wday'].unique()[0]
    if old_wday == 6:
        new_data = new_data.assign(wday=0)
    else:
        new_data = new_data.assign(wday=old_wday + 1)

    # Modifying the column 'wm_yr_wk'.
    old_wm = new_data['wm_yr_wk'].unique()[0]
    wday = new_data['wday'].unique()[0]
    if wday == 0:
        new_data = new_data.assign(wm_yr_wk=old_wm + 1)
    else:
        new_data = new_data

    # Modifying the column 'month'
    new_data = new_data.assign(month=int(new_data['date'].unique()[0][5:7]))

    # Modifying the column 'year'
    new_data = new_data.assign(year=int(new_data['date'].unique()[0][:4]))

    # Modifying the 'event' columns
    new_data = new_events(new_data)

    # Modifying the 'snap' columns
    new_data = new_snaps(new_data)

    # Modifying the 'sell_price' column
    prices = new_data['sell_price'].values.tolist()
    for i in range(0, len(prices)):
        random_numb = round(np.random.uniform(-0.1, 0.1), 2)
        prices[i] = round(prices[i] + random_numb, 2)
    new_data = new_data.assign(sell_price=prices)

    return new_data


def new_events(new_data):
    """

    Parameters
    ----------
    new_data

    Returns
    -------

    """
    with open('events_dictionary.pkl', 'rb') as f:
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


def new_snaps(new_data):
    """

    Parameters
    ----------
    new_data

    Returns
    -------

    """
    with open('snaps_dictionary.pkl', 'rb') as f:
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


