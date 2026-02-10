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
    label_encoder_joblib_path = Path("src/models/label_encoder.joblib")

    scaler = joblib.load(scaler_joblib_path)
    label_encoder = joblib.load(label_encoder_joblib_path)
    X_raw = np.array(current_profile.symptoms).reshape(1, -1)
    X_scaled = scaler.transform(X_raw)

    model = LogisticRegressionModel()
    model.load_model(file_path=logistic_regression_joblib_path)
    predictions = model.predict_top_5(X_scaled, gender=current_profile.sex)

    predicted_classes = [p[0] for p in predictions]
    predicted_classes_array = np.array(predicted_classes).reshape(-1, 1)
    original_labels = label_encoder.inverse_transform(predicted_classes_array)

    speeds_list = []

    for i in range(5):
        disease_name = diseases.diseases[original_labels[i]]
        probability = predictions[i][1]
        percentage = f"{probability:.2%}"
        
        labels[i].setText(f"{i+1}: {disease_name} - {percentage}")

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

def create_results_window():
    global results_window
    if results_window is None:
        results_window = uic.loadUi("src/gui/ui/results_window.ui")
        setup_results_window()

    run_model()

    results_window.show()
    return results_window