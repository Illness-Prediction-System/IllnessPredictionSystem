import joblib

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, f1_score

class LogisticRegressionModel:

    def __init__(self, random_state: int = 15, max_iter: int = 1000):

        self.model = LogisticRegression(random_state=random_state, max_iter=max_iter)



    def train(self, X_train, y_train):

        self.model.fit(X_train, y_train)



    def evaluate(self, X, y):

        y_pred = self.model.predict(X)

        metrics = {

        "accuracy": accuracy_score(y, y_pred),

        "f1_weighted": f1_score(y, y_pred, average='weighted', zero_division=0)

        }

        return metrics



    def save_model(self, file_path: str):

        joblib.dump(self.model, file_path)



    def load_model(self, file_path: str):

        self.model = joblib.load(file_path)

   

    def predict_top_5(self, X):

        probabilities = self.model.predict_proba(X)[0]

        top_5_indices = probabilities.argsort()[-5:][::-1]

        classes = self.model.classes_

        return [(classes[i], probabilities[i]) for i in top_5_indices]