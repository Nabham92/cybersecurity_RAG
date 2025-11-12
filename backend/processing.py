import pandas as pd 
from config import FILE_PATH_DATA
import numpy as np

def clean_metadata(meta):
    """
    Cleans metadata to be compatible  :
    - Gets rid of None
    - Converts nested dicts/lists in str
    """

    if meta is None:
        return {}
    
    if not isinstance(meta, dict):
        return {}

    cleaned = {}

    for k, v in meta.items():
        
        key = str(k)

        if v is None:
            cleaned[key] = ""  
            continue

        if isinstance(v, (list, tuple, np.ndarray)):
            
            if isinstance(v, np.ndarray):
                v = v.tolist()
            
            if len(v) > 10:
                cleaned[key] = str(v[:10]) + "..."  
            else:
                cleaned[key] = str(v)

        elif isinstance(v, dict):
            
            for sub_k, sub_v in v.items():
                sub_key = f"{key}_{sub_k}"
                if sub_v is None:
                    cleaned[sub_key] = ""
                else:
                    cleaned[sub_key] = str(sub_v)  # tout en str pour sécurité

        else:
            #
            cleaned[key] = v

    return cleaned
    
def load_data(N=1000):
    df=pd.read_parquet(FILE_PATH_DATA)
    df["meta"]=df["meta"].apply(clean_metadata)
    df["text"]=df["text"].apply(lambda t : f"passage: {t}")
    return(df.iloc[:N,:])
