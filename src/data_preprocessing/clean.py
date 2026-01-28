import pandas as pd

def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

def normalize_text(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df[column] = (df[column].str.lower().str.strip())
    return df

def clean_dataset(df: pd.DataFrame, text_column = "name") -> pd.DataFrame:
    df = drop_empty_rows(df)
    df = normalize_text(df, column = text_column)
    return df