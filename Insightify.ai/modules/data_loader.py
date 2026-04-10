import pandas as pd
import dask.dataframe as dd
import os

@pd.option_context('mode.use_inf_as_na', True)
def load_file(file_obj):
    file_obj.seek(0, os.SEEK_END)
    file_size_mb = file_obj.tell() / (1024 * 1024)
    file_obj.seek(0)
    
    filename = file_obj.name
    
    if file_size_mb > 500 and filename.endswith('.csv'):
        df = dd.read_csv(file_obj).compute()
    else:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_obj)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_obj)
        elif filename.endswith('.json'):
            df = pd.read_json(file_obj)
            
    return df, file_size_mb
