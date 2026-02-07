from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, accuracy_score

class DecisionTreeModel:
    def __init__(self, random_state: int = 15, max_depth: int = None):
        self.model = DecisionTreeClassifier(random_state=random_state, max_depth=max_depth)

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
        import joblib
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str):
        import joblib
        self.model = joblib.load(file_path)