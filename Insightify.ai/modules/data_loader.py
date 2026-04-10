import pandas as pd
import dask.dataframe as dd
import os

def load_file(file_obj):
    # Get file size
    file_obj.seek(0, os.SEEK_END)
    file_size_mb = file_obj.tell() / (1024 * 1024)
    file_obj.seek(0)
    
    filename = file_obj.name
    
    if filename.endswith('.csv'):
        if file_size_mb > 500:
            # For massive files, we need to save to a temp file first 
            # because Dask cannot read Streamlit memory objects directly.
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                tmp.write(file_obj.getvalue())
                tmp_path = tmp.name
            df = dd.read_csv(tmp_path).compute()
            os.remove(tmp_path) # Clean up
        else:
            try:
                # Attempt 1: Standard UTF-8 comma-separated
                df = pd.read_csv(file_obj)
            except UnicodeDecodeError:
                # Attempt 2: Handle Windows Excel CSVs
                file_obj.seek(0)
                df = pd.read_csv(file_obj, encoding='latin1')
            except pd.errors.ParserError:
                # Attempt 3: Auto-detect weird delimiters (like semicolons)
                file_obj.seek(0)
                df = pd.read_csv(file_obj, sep=None, engine='python')
                
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_obj)
        
    elif filename.endswith('.json'):
        df = pd.read_json(file_obj)
        
    else:
        raise ValueError(f"Unsupported file extension: {filename}")
        
    return df, file_size_mb
