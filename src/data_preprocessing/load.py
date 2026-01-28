import pandas as pd

def load_raw_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)