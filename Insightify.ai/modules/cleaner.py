import pandas as pd
import numpy as np

def auto_clean(df):
    log = []
    
    # 1. Remove duplicates
    initial_shape = df.shape
    df = df.drop_duplicates()
    if initial_shape != df.shape:
        log.append(f"✅ Removed {initial_shape[0] - df.shape[0]} duplicate rows.")
        
    # 2. Handle Missing Values
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna(df[col].mode()[0])
                log.append(f"✅ Imputed {missing} missing categorical values in '{col}' with mode.")
            else:
                df[col] = df[col].fillna(df[col].median())
                log.append(f"✅ Imputed {missing} missing numerical values in '{col}' with median.")
                
    # 3. Handle Extreme Outliers (IQR Method)
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
        
    log.append("✅ Capped extreme numeric outliers to prevent skewed charts.")
    return df, log
