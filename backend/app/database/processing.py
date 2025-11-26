import pandas as pd 
from backend.config import FILE_PATH_DATA
import numpy as np

import re

def clean_text(raw: str) -> str:
    """
    Clean raw CVE text from NVD/VulDB-like sources.
    Removes noise and keeps only essential security information.
    """

    text = raw.strip()

    # 1. Remove the entire References section
    text = re.sub(r"References:\s*-.*", "", text, flags=re.DOTALL)

    # 2. Remove URLs everywhere
    text = re.sub(r"https?://\S+", "", text)

    # 3. Remove product marketing text like "[Product]"
    text = re.sub(r"\[.*?\]", "", text)

    # 4. Remove long file paths except keep last filename (optional)
    # e.g. /foo/bar/baz.php → baz.php
    text = re.sub(r"/[\w\-./]+/([\w\-]+\.php)", r"\1", text)

    # 5. Remove repeated whitespace / newlines
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # 6. Remove prefixes "passage:" etc.
    text = text.replace("passage:", "").strip()

    # 7. Extract ONLY important sections
    keep_sections = []

    # CVE Header line
    header_match = re.search(r"(CVE-\d{4}-\d+.*)", text)
    if header_match:
        keep_sections.append(header_match.group(1))

    # Weaknesses (CWE)
    cwe_match = re.search(r"Weaknesses:\s*(.*)", text)
    if cwe_match:
        keep_sections.append("Weaknesses: " + cwe_match.group(1))

    # Affected product
    affected_match = re.search(r"Affected:\s*(.*)", text)
    if affected_match:
        keep_sections.append("Affected: " + affected_match.group(1))

    # Description block (cleaned)
    desc = ""
    desc_match = re.search(r"Description:\s*(.*)", text, flags=re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()

        # remove sentences mentioning exploits being published
        desc = re.sub(r"The exploit .*?\. ?", "", desc)

        # remove redundant boilerplate
        desc = re.sub(r"It has been .*?\. ?", "", desc)
        desc = re.sub(r"The vendor .*?\. ?", "", desc)

        keep_sections.append("Description: " + desc)

    # 8. Join clean sections
    cleaned = "\n".join(keep_sections).strip()

    return cleaned


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
    df["text"]=df["text"].apply(clean_text)
    
    return(df.iloc[:N,:])
