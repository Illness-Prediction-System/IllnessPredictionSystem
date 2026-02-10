import sys
from PyQt6 import QtWidgets
from src.gui.controllers.main_window_controller import setup_main_window

main_window = None

def create_close_handler(app):
    def close_event(event):
        app.quit()
    return close_event

def main():
    global main_window
    app = QtWidgets.QApplication(sys.argv)
    main_window = setup_main_window()
    
    main_window.closeEvent = create_close_handler(app)
    
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()