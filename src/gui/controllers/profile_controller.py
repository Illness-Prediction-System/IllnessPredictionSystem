from PyQt6 import QtWidgets, uic
from src.data_for_application.user_data import current_profile

profile_window = None
symptoms_button = None

profile_status_label = None

first_name_line = None
last_name_line = None
age_line = None
sex_combobox = None
confirm_button = None
requirement_label = None

def update_status(value):
    if value:
        profile_status_label.setText("Profile created.")
        profile_status_label.setStyleSheet("color: green;")
    else:
        profile_status_label.setStyleSheet("color: blue;")

def save_profile():
    symptoms_button.setEnabled(False)

    if first_name_line.text() == "" or last_name_line.text() == "":
        requirement_label.setText("Please enter your full name.")
        update_status(False)
        return

    if age_line.text() == "":
        requirement_label.setText("Please enter your age.")
        update_status(False)
        return

    if not (age_line.text().isdigit() and int(age_line.text()) >= 0):
        requirement_label.setText("Age must be an integer.")
        update_status(False)
        return

    requirement_label.setText("Profile has been created")
    profile_window.hide()

    current_profile.first_name = first_name_line.text()
    current_profile.last_name = last_name_line.text()
    current_profile.age = int(age_line.text())
    current_profile.sex = sex_combobox.currentText()

    update_status(True)
    symptoms_button.setEnabled(True)

def setup_profile_window():
    global first_name_line, last_name_line, age_line, sex_combobox, confirm_button, requirement_label
    first_name_line = profile_window.findChild(QtWidgets.QLineEdit, "leFirstName")
    last_name_line = profile_window.findChild(QtWidgets.QLineEdit, "leLastName")
    age_line = profile_window.findChild(QtWidgets.QLineEdit, "leAge")
    sex_combobox = profile_window.findChild(QtWidgets.QComboBox, "cmbSex")
    confirm_button = profile_window.findChild(QtWidgets.QPushButton, "btnConfirm")
    requirement_label = profile_window.findChild(QtWidgets.QLabel, "lblRequirement")

    confirm_button.clicked.connect(save_profile)

def create_profile_window(button=None, status=None):
    global profile_window, symptoms_button, profile_status_label

    symptoms_button = button
    profile_status_label = status

    if profile_window is None:
        profile_window = uic.loadUi("src/gui/ui/profile_window.ui")
        setup_profile_window()

    profile_window.show()
    return profile_window