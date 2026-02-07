from src.database import get_table, create_connection_pool, close_connection_pool 
import pandas as pd


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
    create_connection_pool()
    names = ["case_symptoms", "diseases", "medical_cases", "patients", "symptoms"]
    tables = {name : get_table(name) for name in names}
    close_connection_pool()
    df = get_merged(tables)
    return df

if __name__ == "__main__":
    build_dataset()