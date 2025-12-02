#!/usr/bin/env python
# coding: utf-8

# In[65]:


get_ipython().run_line_magic('pip', 'install pandas')


# In[66]:


import sys 
from pathlib import Path


project_root = None
for p in Path.cwd().resolve().parents:
    if (p / "utils").exists() and (p / "data").exists():
        project_root = p
        break

if project_root is None:
    raise RuntimeError("Raíz no encontrada.")

sys.path.insert(0, str(project_root))


# In[67]:


import logging
import numpy as np
import pandas as pd
from utils.paths import find_project_root

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)s | %(message)s"
)

project_root = None
for p in Path.cwd().resolve().parents:
    if (p / "utils").exists() and (p / "data").exists():
        project_root = p
        break

if project_root is None:
    logging.error("No se encontró la raíz del proyecto")
    raise RuntimeError("Raíz no encontrada.")

logging.info(f"Raiz encontrada en {project_root}")
sys.path.insert(0, str(project_root))


# ### Extraemos y vemos la información pura del csv almacenado

# In[68]:


root = find_project_root()
csv_path = root / "data" / "raw" / "job_market.csv"


df = pd.read_csv(csv_path)
df.info()


# In[69]:


raw_backup_path = root / "data" / "raw" / "job_market_raw_backup.csv"
df.to_csv(raw_backup_path, index=False)


# ### Tratamiento de datos almacenados dentro del csv 

# In[70]:


def drop_columns(df):
    cols_to_drop=['company_rating','company_reviews_count', 'experience_range', 'skills', 'vacancy_count', 'work_from_home_type']
    existing = [cols for cols in cols_to_drop if cols in df.columns]
    df = df.drop(columns=existing)
    return df



# In[71]:


def dedupe_jobs(df):
    key = 'id' if 'id' in df.columns else 'job_url'
    if 'created' in df.columns:
        df = df.sort_values('created', ascending=False)
    df = df.drop_duplicates(subset=[key], keep='first')
    return df


# In[72]:


def normalize_string_column(df, col):
    if col not in df.columns:
        return df

    df[col] = df[col].replace([float("inf"), float("-inf")], None)

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .replace({"nan": None, "None": None, "": None, "inf": None, "-inf": None})
    )
    df[col] = df[col].where(df[col].notna(), None)
    return df


# In[73]:


def rename_columns(df):
    rename_mapping = {
                        'job_url':'url',
                        'company_addresses':'address',
                        'company_industry':'industry',
                        'company_logo':'logo',
                        'company_num_employees':'num_employees',
                        'company_rating':'rating',
                        'company_revenue':'revenue',
                        'company_reviews_count':'reviews_count',
                        'job_url_direct':'url_direct',
                        'created_at':'created',
                        'is_remote':'remote',
                        'job_function': 'role',
                        'job_level':'seniority',
                        'listing_type':'listing',
                        'title':'job_title'
                     }
    rename_map = {k: v for k, v in rename_mapping.items() if k in df.columns}
    df = df.rename(columns=rename_map)
    return df


# In[74]:


def change_values(df):
  date_cols = ["created", "date_posted"]
  for col in date_cols:
    if col in df.columns:
      df[col] = pd.to_datetime(
        df[col],
        errors="coerce",
        utc=True
      )
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.where(df.notna(), None)
  return df


# In[79]:


def convert_timestamps(df):
    for col in df.columns:
        if pd.api.types.is_datetime64tz_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
        elif pd.api.types.is_datetime64_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
    return df



# In[75]:


def add_missing_flags(df, columns):
    for col in columns:
        if col in df.columns:
            is_all_na = df[col].isna().all()
            is_any_na = df[col].isna().any()
            if is_any_na and not is_all_na:
                df[f"{col}_missing"] = df[col].isna().astype(int)
    return df


# ## Muestra el df limpio

# In[ ]:


df_proccesed = drop_columns(df)
df_proccesed = dedupe_jobs(df_proccesed)
columns_to_normalize = ["company", "address", "company_description", "industry", 
                        "logo", "num_employees", "revenue", "company_url", 
                        "company_url_direct", "currency", "date_posted", "description", 
                        "emails", "interval", "role", "seniority", "job_type", "url_direct", 
                        "listing", "location", "min_amount", "max_amount"]
for col in columns_to_normalize:
	df_proccesed = normalize_string_column(df_proccesed, col)
df_proccesed = rename_columns(df_proccesed)
df_proccesed = change_values(df_proccesed)
df_proccesed = convert_timestamps(df_proccesed)
df_proccesed = add_missing_flags(df_proccesed, ["company", "company_url", "location", "max_amount", "min_amount", "listing"])  

df_proccesed.info()


# In[77]:


df_proccesed.head(2)


# In[78]:


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

root = find_project_root()


csv_path = root / "data" / "processed" / "job_market_processed.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)

logging.info(f"Ruta {root} encontrada.")
logging.info(f"CSV exportado hacia {csv_path}")

job_processed_path = root / "data" / "processed" / "job_market_processed.csv" 
df_proccesed.to_csv(job_processed_path, index=False, encoding="utf-8")

logging.info(f"CSV creado en {csv_path.relative_to(root)}")

