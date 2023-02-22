import pandas as pd
import preprocessing

path = '../../extracted.csv'
dataset = pd.read_csv(path)

del_attr = ['id', 'item_id', 'dept_id', 'store_id', 'd', 'wm_yr_wk', 'weekday', 'year']  # Keep 'date' attribute

classification = True
prepared_set = preprocessing.preprocessing_pipeline(dataset, del_attr, classification)
if classification:
    prepared_set.to_csv('/save_volume/preprocessed_data_cls.csv')
else:
    prepared_set.to_csv('/save_volume/preprocessed_data.csv')

    
