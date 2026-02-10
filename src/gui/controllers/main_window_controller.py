from PyQt6 import QtWidgets, uic

from src.gui.controllers.profile_controller import create_profile_window
from src.gui.controllers.symptoms_controller import create_symptoms_window
from src.gui.controllers.results_controller import create_results_window

from src.gui.controllers.image_loader import load_main_images

profile_button = None
symptoms_button = None
results_button = None
profile_status_label = None
symptoms_status_label = None

def set_symptoms_button_state(state):
    symptoms_button.setEnabled(state)

def setup_main_window():   
    global profile_button, symptoms_button, results_button

    main_window = QtWidgets.QMainWindow()
    uic.loadUi("src/gui/ui/main_window.ui", main_window)
    
    profile_button = main_window.findChild(QtWidgets.QPushButton, "btnProfile")
    symptoms_button = main_window.findChild(QtWidgets.QPushButton, "btnSymptoms")
    results_button = main_window.findChild(QtWidgets.QPushButton, "btnResults")
    profile_status_label = main_window.findChild(QtWidgets.QLabel, "lblProfileStatus")
    symptoms_status_label = main_window.findChild(QtWidgets.QLabel, "lblSymptomsStatus")

    symptoms_button.setEnabled(False)
    results_button.setEnabled(False)
    
    profile_button.clicked.connect(lambda: create_profile_window(button=symptoms_button, status=profile_status_label))
    symptoms_button.clicked.connect(lambda: create_symptoms_window(button=results_button, status=symptoms_status_label))
    results_button.clicked.connect(create_results_window)
    
    load_main_images(main_window)
    
    return main_window