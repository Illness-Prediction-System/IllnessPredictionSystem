import joblib, json

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, top_k_accuracy_score
from pathlib import Path

class LogisticRegressionModel:

    def __init__(self, random_state: int = 15, max_iter: int = 300):
        self.model = LogisticRegression(
            random_state=random_state, 
            max_iter=max_iter,
            solver='lbfgs',
            C=1.0,
        )

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X)
        y_proba = self.model.predict_proba(X)
        metrics = {
            "accuracy": accuracy_score(y, y_pred),
            "top_2_accuracy": top_k_accuracy_score(y, y_proba, k=2, labels=self.model.classes_),
            "top_3_accuracy": top_k_accuracy_score(y, y_proba, k=3, labels=self.model.classes_),
            "top_4_accuracy": top_k_accuracy_score(y, y_proba, k=4, labels=self.model.classes_),
            "top_5_accuracy": top_k_accuracy_score(y, y_proba, k=5, labels=self.model.classes_),
            "f1_weighted": f1_score(y, y_pred, average='weighted', zero_division=0)
        }
        return metrics

    def save_model(self, file_path: str):
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str):
        self.model = joblib.load(file_path)

    def predict_top_5(self, X, gender='both'):
        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_
        
        mapping_path = Path("data/mappings/label_mapping_gender.json")
        with open(mapping_path, 'r', encoding='utf-8') as f:
            gender_mapping = json.load(f)

        filtered_results = []
        
        for i, prob in enumerate(probabilities):
            class_name = classes[i]
            target_gender = gender_mapping.get(class_name, {}).get("gender_specific", "both")
            
            if target_gender == "both" or target_gender == gender:
                filtered_results.append((class_name, prob))

        filtered_results.sort(key=lambda x: x[1], reverse=True)

        return filtered_results[:5]