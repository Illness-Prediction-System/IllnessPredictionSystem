from src.data_preprocessing import load_parquet
import pandas as pd
from pathlib import Path

def show_schema(path):
    df = load_parquet(path)
    print(df.head(10))

if __name__ == "__main__":
    names = ["case_symptoms", "diseases", "medical_cases", "patients", "symptoms"]
    for name in names:
        path = Path(f"data/preprocessed/{name}.parquet")
        show_schema(path)
        print()