from PyQt6 import QtWidgets, uic
from pathlib import Path
from src.models.logistic_regression import LogisticRegressionModel
from src.data_for_application import symptoms, diseases
from src.data_for_application.user_data import current_profile
from src.gui.controllers import windrose

import joblib
import numpy as np

results_window = None

labels = [None] * 5
windrose_frame = None

def run_model():
    scaler_joblib_path = Path("src/models/scaler.joblib")
    logistic_regression_joblib_path = Path("src/models/logistic_regression.joblib")

    scaler = joblib.load(scaler_joblib_path)
    X_raw = np.array(current_profile.symptoms).reshape(1, -1)
    X_scaled = scaler.transform(X_raw)

    model = LogisticRegressionModel()
    model.load_model(file_path=logistic_regression_joblib_path)
    predictions = model.predict_top_5(X_scaled)

    speeds_list = []

    for i in range(5):
        disease_name = f"{i}: {diseases.diseases[predictions[i][0]]}"
        probability = predictions[i][1]
        percentage = f"{probability:.2%}"
        
        labels[i].setText(f"{disease_name}: {percentage}")

        speeds_list.extend([probability])

    windrose.create_windrose_in_frame(windrose_frame, speeds_list)
    
def setup_results_window():
    global labels, windrose_frame
    labels[0] = results_window.findChild(QtWidgets.QLabel, "lblFirst")
    labels[1] = results_window.findChild(QtWidgets.QLabel, "lblSecond")
    labels[2] = results_window.findChild(QtWidgets.QLabel, "lblThird")
    labels[3] = results_window.findChild(QtWidgets.QLabel, "lblFourth")
    labels[4] = results_window.findChild(QtWidgets.QLabel, "lblFifth")
    windrose_frame = results_window.findChild(QtWidgets.QFrame, "frmWindrose")

    run_model()

def create_results_window():
    global results_window
    if results_window is None:
        results_window = uic.loadUi("src/gui/ui/results_window.ui")
        setup_results_window()

    results_window.show()
    return results_window