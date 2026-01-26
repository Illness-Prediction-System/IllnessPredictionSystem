import pandas as pd

def build_label_map(labels) -> dict:
    return {label: idx for idx, label in enumerate(labels)}

def encode_labels(df: pd.DataFrame, label_column="label"):
    label_map = build_label_map(df[label_column].unique())
    df[f"{label_column}_id"] = df[label_column].map(label_map)
    return df, label_map