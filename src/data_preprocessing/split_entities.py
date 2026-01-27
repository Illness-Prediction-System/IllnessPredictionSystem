import pandas as pd
import numpy as np
import uuid
from pathlib import Path
from typing import Dict, Any
from faker import Faker

def split_entities(df: pd.DataFrame, disease_config: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    fake = Faker()
    df = df.copy()
    diagnosis_col = df.columns[0]
    patient_cols = ['patient_id', 'gender', 'first_name', 'last_name', 'age']
    symptom_cols = [col for col in df.columns[1:] if col not in patient_cols and col != f"{diagnosis_col}_id"]

    disease_info = {}
    unique_disease_names = df[diagnosis_col].unique()
    
    diseases_data = []
    for name in unique_disease_names:
        config = disease_config.get(name, {"mapping": 0, "gender_specific": "both"})
        d_id = str(uuid.uuid4())
        g_spec = config.get("gender_specific", "both")
        
        disease_info[name] = {"id": d_id, "gender": g_spec}
        diseases_data.append({
            'disease_id': d_id,
            'code': config.get('mapping'),
            'name': name,
            'gender': g_spec
        })

    for idx, row in df.iterrows():
        req_gender = disease_info[row[diagnosis_col]]["gender"]
        curr_gender = row["gender"]
        
        needs_fix = (req_gender == "male" and curr_gender == "F") or \
                    (req_gender == "female" and curr_gender == "M")
        
        if needs_fix:
            new_gender = "M" if req_gender == "male" else "F"
            new_first_name = fake.first_name_male() if new_gender == "M" else fake.first_name_female()
            
            df.at[idx, "gender"] = new_gender
            df.at[idx, "first_name"] = new_first_name

    patients_df = df[patient_cols].drop_duplicates(subset=['patient_id']).reset_index(drop=True)
    diseases_df = pd.DataFrame(diseases_data)
    
    symptoms_df = pd.DataFrame({
        'symptom_id': range(1, len(symptom_cols) + 1),
        'symptom_name': symptom_cols
    })
    symptom_map = dict(zip(symptoms_df['symptom_name'], symptoms_df['symptom_id']))

    medical_cases = []
    case_symptoms = []

    for idx, row in df.iterrows():
        case_id = idx + 1
        d_name = row[diagnosis_col]
        
        medical_cases.append({
            'case_id': case_id,
            'patient_id': row['patient_id'],
            'disease_id': disease_info[d_name]["id"]
        })

        for s_name in symptom_cols:
            if row[s_name] == 1:
                case_symptoms.append({
                    'case_id': case_id,
                    'symptom_id': symptom_map[s_name],
                    'value': 1
                })

    return {
        'patients': patients_df,
        'diseases': diseases_df,
        'symptoms': symptoms_df,
        'medical_cases': pd.DataFrame(medical_cases),
        'case_symptoms': pd.DataFrame(case_symptoms)
    }


def save_split_data(entities: Dict[str, pd.DataFrame], output_dir: Path):
    for name, df in entities.items():
        path = output_dir / f"{name}.parquet"
        df.to_parquet(path, index=False, engine="pyarrow")