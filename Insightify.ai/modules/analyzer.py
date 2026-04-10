import pandas as pd

def get_basic_stats(df):
    """Returns a clean dataframe of descriptive statistics."""
    # describe() returns stats for numeric columns
    stats = df.describe().T
    
    # Add a column for missing value percentage
    stats['missing_%'] = (df.isnull().sum() / len(df) * 100).round(2)
    
    return stats
