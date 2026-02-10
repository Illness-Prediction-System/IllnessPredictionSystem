from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets

def load_main_images(window):
    for txt in ["Profile", "Results", "Symptoms"]:
        label = window.findChild(QtWidgets.QLabel, f"lbl{txt}")
        if label:
            pixmap = QPixmap(f"resources/images/{txt.lower()}.png")
            label.setPixmap(pixmap)