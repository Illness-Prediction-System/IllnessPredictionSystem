import joblib
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score

class XGBoostModel:
    def __init__(self, random_state: int = 15, n_estimators: int = 100):
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            objective='multi:softprob',
            num_class=773,
            learning_rate=0.05,
            max_depth=10,         # Не даємо деревам роздуватися
            tree_method='hist',  # Економить купу оперативки
            device='cpu',
            n_jobs=-1,
            gamma=0.1,           # Допомагає боротися з перенавчанням
            subsample=0.8,       # Кожне дерево бачить тільки 80% пацієнтів
            colsample_bytree=0.8 # Кожне дерево бачить тільки 80% симптомів
        )

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X)
        metrics = {
            "accuracy": accuracy_score(y, y_pred),
            "f1_weighted": f1_score(y, y_pred, average='weighted', zero_division=0)
        }
        return metrics

    def predict_top_5(self, X):
        probabilities = self.model.predict_proba(X)[0]
        top_5_indices = probabilities.argsort()[-5:][::-1]
        classes = self.model.classes_
        return [(classes[i], probabilities[i]) for i in top_5_indices]

    def save_model(self, file_path: str):
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str):
        self.model = joblib.load(file_path)