from pathlib import Path
import pandas as pd
from src.data_for_models import build_dataset, prepare_data, scale_data
from src.models.logistic_regression import LogisticRegressionModel
from src.models.decision_tree import DecisionTreeModel
from src.models.random_forest import RandomForestModel
from src.models.xgboost import XGBoostModel

def run_pipeline():
    dataset = build_dataset()
    BASE_MODELS_PATH = Path(__file__).resolve().parent / "models"
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_data(dataset, target_column='code')
    
    X_train_scaled, X_val_scaled, X_test_scaled = scale_data(X_train, X_val, X_test)
    
    models = {
        "Logistic Regression": LogisticRegressionModel(random_state=15, max_iter=300),
        #"Decision Tree": DecisionTreeModel(random_state=15, max_depth=500),
        #"Random Forest": RandomForestModel(random_state=15, n_estimators=25),
        #"XGBoost": XGBoostModel(random_state=15, n_estimators=100)
    }
    results = {}

    for name, model_obj in models.items():
        print(f"Training {name}...")
        model_obj.train(X_train_scaled, y_train)
        
        report = model_obj.evaluate(X_val_scaled, y_val)
        results[name] = report
        
        model_filename = f"{name.lower().replace(' ', '_')}.joblib"
        full_path = str(BASE_MODELS_PATH / model_filename)
        
        model_obj.save_model(full_path)
        print(f"Saved to: {full_path}")

    df_results = pd.DataFrame(results).transpose()
    print(df_results)

if __name__ == "__main__":
    run_pipeline()