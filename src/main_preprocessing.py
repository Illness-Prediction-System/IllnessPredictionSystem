import pandas as pd
import json
from pathlib import Path
from src.scripts import generate_patients
from src.data_preprocessing import (
    load_raw_csv,
    clean_dataset,
    encode_labels,
    split_entities,
    save_split_data
)

def run_pipeline():
    raw_data_path = Path("data/raw/dataset.csv")
    output_dir = Path("data/preprocessed")
    mappings_dir = Path("data/mappings")
    mapping_gender_path = mappings_dir / "label_mapping_gender.json"
    label_mapping_output = mappings_dir / "label_mapping.json"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    mappings_dir.mkdir(parents=True, exist_ok=True)

    df = load_raw_csv(raw_data_path)
    df = clean_dataset(df, text_column=df.columns[0])
    
    df, labels = encode_labels(df, label_column=df.columns[0])
    
    with open(label_mapping_output, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)
    
    with open(mapping_gender_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    patients_df = pd.DataFrame(generate_patients())
    df = pd.concat([df, patients_df], axis=1)

    entities = split_entities(df=df, disease_config=config_data)
    save_split_data(entities, output_dir)
    

if __name__ == "__main__":
    run_pipeline()