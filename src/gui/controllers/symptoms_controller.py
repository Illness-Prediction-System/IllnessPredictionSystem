from PyQt6 import QtCore, QtWidgets, uic
from src.data_for_application import symptoms
from src.data_for_application.user_data import current_profile

symptoms_window = None
results_button = None

categories_list = None
symptoms_list = None
selected_list = None
confirm_button = None
search_line_edit = None
progress_bar = None
requirement_label = None

symptoms_status_label = None

selected_category = "All"

def update_status(value):
    results_button.setEnabled(value)
    if value:
        symptoms_status_label.setStyleSheet("color: green;")
        symptoms_status_label.setText("Symptoms")
    else:
        symptoms_status_label.setStyleSheet("color: blue;")
        symptoms_status_label.setText("No profile")

def save_symptoms():
    if progress_bar.value() < 100:
        update_status(False)
        return

    for index, symptom in enumerate(symptoms.contents["All"]):
        if selected_list.findItems(symptom, QtCore.Qt.MatchFlag.MatchExactly):
            current_profile.symptoms[index] = 1
        else:
            current_profile.symptoms[index] = 0
        
    symptoms_window.hide()
    update_status(True)

def search_symptoms_list(search_text):
    symptoms_list.clear()
    
    for symptom in symptoms.contents[selected_category]:
        if search_text.lower() in symptom.lower():
            symptoms_list.addItem(symptom)

def filter_symptoms_list(item):
    global selected_category
    selected_category = item.text()
    
    symptoms_list.clear()
    symptoms_list.addItems(symptoms.contents[selected_category])

def insert_symptom(item):
    if selected_list.findItems(item.text(), QtCore.Qt.MatchFlag.MatchExactly):
        return

    selected_list.addItem(item.text())

    progress_bar.setValue(selected_list.count() * 20)

    if progress_bar.value() == 100:
        requirement_label.setText("You can now proceed to the results window.")
        confirm_button.setEnabled(True)

def remove_symptom(item):
    selected_list.takeItem(selected_list.currentRow())

    progress_bar.setValue(selected_list.count() * 20)

    if progress_bar.value() < 100:
        requirement_label.setText("Choose at least five symptoms")
        confirm_button.setEnabled(False)
        update_status(False)

def populate_categories_list(sex):
    categories_list.clear()

    categories_list.addItems(symptoms.contents)

    item = None

    if sex=="Male":
        item = categories_list.findItems("Female reproduction", QtCore.Qt.MatchFlag.MatchExactly)
    else:
        item = categories_list.findItems("Male reproduction", QtCore.Qt.MatchFlag.MatchExactly)

    row = categories_list.row(item[0])
    categories_list.takeItem(row)

def populate_symptoms_list():
    symptoms_list.addItems(symptoms.contents["All"])

def setup_symptoms_window():
    global categories_list, symptoms_list, selected_list, confirm_button, search_line_edit, progress_bar, requirement_label
    categories_list = symptoms_window.findChild(QtWidgets.QListWidget, "lstCategories")
    symptoms_list = symptoms_window.findChild(QtWidgets.QListWidget, "lstSymptoms")
    selected_list = symptoms_window.findChild(QtWidgets.QListWidget, "lstSelected")
    confirm_button = symptoms_window.findChild(QtWidgets.QPushButton, "btnConfirm")
    search_line_edit = symptoms_window.findChild(QtWidgets.QLineEdit, "leSearch")
    progress_bar = symptoms_window.findChild(QtWidgets.QProgressBar, "pbarSymptoms")
    requirement_label = symptoms_window.findChild(QtWidgets.QLabel, "lblRequirement")

    confirm_button.setEnabled(False)

    categories_list.itemActivated.connect(filter_symptoms_list)
    symptoms_list.itemActivated.connect(insert_symptom)
    selected_list.itemActivated.connect(remove_symptom)
    search_line_edit.textChanged.connect(search_symptoms_list)
    confirm_button.clicked.connect(save_symptoms)

    populate_categories_list(current_profile.sex)
    populate_symptoms_list()

def create_symptoms_window(button=None, status=None):
    global symptoms_window, results_button, symptoms_status_label

    results_button = button
    symptoms_status_label = status
    
    if symptoms_window is None:
        symptoms_window = uic.loadUi("src/gui/ui/symptoms_window.ui")
        setup_symptoms_window()

    symptoms_window.show()
    return symptoms_window