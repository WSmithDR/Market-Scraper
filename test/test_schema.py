import re
import sys 
import pytest
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
from utils.paths import find_project_root
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
from utils.paths import find_project_root

root = find_project_root()

csv_path = root / "data" / "processed" / "job_market_processed.csv"
expected_columns = {
        "url", "company", "address", "description", "industry", 
        "logo","num_employees", "revenue", "company_url", "company_url_direct", 
        "created", "currency", "date_posted", "description", "emails", 
        "id", "interval", "remote", "role", "seniority", "job_type", "url_direct", 
        "listing", "location", "max_amount", "min_amount", "salary_source", 
        "site", "job_title", "company_missing","company_url_missing",
        "location_missing", "max_amount_missing", "min_amount_missing", "listing_missing"
}


@pytest.fixture(scope="module")
def df():
    parse_dates = ["created", "date_posted"]
    df = pd.read_csv(csv_path, parse_dates=parse_dates, low_memory=False)
    df.columns = df.columns.str.strip()
    text_cols = ["company", "job_title", "location", "company_url"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", pd.NA)
    for date_col in parse_dates:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], utc=True, errors="coerce")

    return df
    
def is_valid_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    if url.strip() == "":
        return False
    pattern = re.compile(
        r"^(http|https)://"
        r"[A-Za-z0-9._\-]+"
        r"(/.*)?$"
    )
    return bool(pattern.match(url))
    
def test_expected_columns(df):
   missing = expected_columns - set(df.columns)
   assert not missing, f"Faltan columnas necesarias: {missing}"
   
def test_required_non_null(df):
    required = {"id": 1.0, 
                "job_title": 0.98, 
                "url": 1.0, 
                "site": 1.0
            }
    for col, min_ratio in required.items():
        assert col in df.columns, f"{col} no está en el DataFrame"
        non_null_count = df[col].notna().sum()
        ratio = non_null_count / len(df)
        assert ratio >= min_ratio, (
            f"{col} tiene muchos valores nulos"
            f"{ratio:.1%} valido vs mínimo {min_ratio:.1%}"
        ) 
        
def test_id_unique(df):
    ids = df["id"].astype(str).str.strip()
    assert ids.is_unique, "ID's duplicados detectados"
   
def test_job_url_unique(df):
    urls = df["url"].astype(str).str.strip()
    assert urls.is_unique, "URL's duplicados detectados"
   
def test_dates_are_valid(df):
    for date_col in ["created", "date_posted"]:
        assert date_col in df.columns, f"Falta columna {date_col}"
        is_dt = pd.api.types.is_datetime64_any_dtype(df[date_col])
        assert is_dt, f"{date_col} no es datetime (dtype actual: {df[date_col].dtype})"
        
def test_salary_field_numeric(df):
    df["min_n"] = pd.to_numeric(df["min_amount"], errors="coerce")
    df["max_n"] = pd.to_numeric(df["max_amount"], errors="coerce")
    assert df["min_n"].notna().any() or df["max_n"].notna().any(), "No existe un salario numérico"
    mask = df["min_n"].notna() & df["max_n"].notna()
    if mask.any():
        assert (df.loc[mask, "min_n"] <= df.loc[mask, "max_n"]).all(), "Existen filas donde min_amount > max_amount"

def test_binary_flags(df):  
    flags = {"company_missing", "company_url_missing", 
             "location_missing", "min_amount_missing",
             "max_amount_missing"}
    for f in flags:
        if f not in df.columns:
            pytest.skip(f"{f} no existe en el dataset")
        vals = df[f].dropna().astype(int).unique()
        allowed = {0, 1}
        assert set(vals).issubset(allowed), f"{f} tiene valores inesperados {vals}"
        
def test_company_flag_consistency(df):
    if "company_missing" in df.columns and "company" in df.columns:
        comp_missing = df["company_missing"].fillna(0).astype(int)
        is_null = df["company"].isna() | (df["company"].astype(str).str.strip() == "")
        assert (comp_missing == is_null.astype(int)).all(), "company_missing no coincide con company.isna()"
                    
def test_url_format(df):
    assert "url" in df.columns, f"Falta columna {url} en el DataFrame"

    invalid_rows = df[~df["url"].apply(is_valid_url)]

    assert invalid_rows.empty, (
        f"Hay {len(invalid_rows)} URLs inválidas.\n"
        f"Ejemplos:\n{invalid_rows['url'].head(5).tolist()}"
    )
   
  



    

