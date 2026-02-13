from urllib import response
import requests
import time
import pandas as pd
import os


def get_merged(entities: dict) -> pd.DataFrame:
    df = entities["medical_cases"].copy()
    df = df.merge(entities["patients"], on="patient_id", how="left")
    df = df.merge(entities["diseases"], on="disease_id", how="left")

    symptoms_expanded = entities["case_symptoms"].merge(entities["symptoms"], on="symptom_id", how="left")
    symptom_pivot = symptoms_expanded.pivot(index="case_id", columns="symptom_name", values="value").fillna(0).astype(int)
    
    final_df = df.merge(symptom_pivot, left_on="case_id", right_index=True, how="left")
    
    symptom_names = entities['symptoms']['symptom_name'].tolist()
    existing_cols = [c for c in final_df.columns if c not in symptom_names]
    final_df = final_df.reindex(columns=existing_cols + symptom_names)
    final_df[symptom_names] = final_df[symptom_names].fillna(0).astype(int)
    
    cols_to_drop = ["case_id", "patient_id", "disease_id", "age", "gender_x", "gender_y", "first_name", "last_name", "name"]
    final_df = final_df.drop(columns=[c for c in cols_to_drop if c in final_df.columns])
    
    return final_df

def build_dataset():
    names = ["case_symptoms", "diseases", "medical_cases", "patients", "symptoms"]
    tables = {}
    for name in names:
        try:
            url = f"http://35.158.139.26:8000/download_table/{name}"
            with requests.get(url, stream=True, timeout=600) as response:
                response.raise_for_status()
                with open(f"{name}.csv", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            tables[name] = pd.read_csv(f"{name}.csv")
            print(f"Fetched {name} successfully.")
            if os.path.exists(f"{name}.csv"):
                os.remove(f"{name}.csv")
            time.sleep(1.5)
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            return None
    df = get_merged(tables)
    return df

if __name__ == "__main__":
    df = build_dataset()
    print(df.head())