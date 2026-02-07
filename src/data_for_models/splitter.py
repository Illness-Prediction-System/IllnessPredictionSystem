from pathlib import Path
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

def prepare_data(df: pd.DataFrame, target_column: str, oversample: bool = False, random_state: int = 15):
    class_counts = df[target_column].value_counts()
    classes_to_keep = class_counts[class_counts >= 7].index
    df = df[df[target_column].isin(classes_to_keep)].copy()

    le = LabelEncoder()
    df[target_column] = le.fit_transform(df[target_column])
    base_path = Path(__file__).resolve().parent.parent
    model_path = base_path / "models"
    joblib.dump(le, model_path / "label_encoder.joblib")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=random_state, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=random_state, stratify=y_temp)

    if oversample:
        ros = RandomOverSampler(random_state=random_state)
        X_train, y_train = ros.fit_resample(X_train, y_train)
    return X_train, X_val, X_test, y_train, y_val, y_test

def scale_data(X_train, X_val, X_test):
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    base_path = Path(__file__).resolve().parent.parent
    model_path = base_path / "models"
    joblib.dump(scaler, model_path / "scaler.joblib")
    
    return X_train_scaled, X_val_scaled, X_test_scaled