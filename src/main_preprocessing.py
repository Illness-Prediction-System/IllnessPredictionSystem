import json
from pathlib import Path
from src.data_preprocessing import (
    load_raw_csv,
    clean_dataset,
    encode_labels
)

def run_pipeline():
    raw_data_path = Path("data/raw/dataset.csv")
    mappings_dir = Path("data/mappings")
    
    df = load_raw_csv(raw_data_path)
    df = clean_dataset(df, text_column=df.columns[0])
    df, labels = encode_labels(df, label_column=df.columns[0])
    mapping_path = mappings_dir / "label_mapping.json"
    with open(mapping_path, "w", encoding="utf-8") as f:
        json_label_map = {str(k): v for k, v in labels.items()}
        json.dump(json_label_map, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    run_pipeline()