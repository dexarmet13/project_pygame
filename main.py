import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QDesktopWidget,
    QMessageBox,
)
from PIL import Image
from PyQt5 import QtCore, QtWidgets
from pathlib import Path
from welcome_window_ui import WelcomeWindowUI
from settings_ui import SettingsUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Welcome Window")
        self.resize_window()
        self.center()

        self.main_stacked_widget = QStackedWidget()
        self.set_background_stylesheet("./src/nekoxl-24218398-766542997.png")
        self.setCentralWidget(self.main_stacked_widget)

        self.welcome_window = WelcomeWindowUI()
        self.welcome_window.settings_button.clicked.connect(self.settings)

        self.main_stacked_widget.addWidget(self.welcome_window)
        self.main_stacked_widget.setCurrentWidget(self.welcome_window)

        self.settings_window = SettingsUI()
        self.settings_window.back_button.clicked.connect(self.go_back)

    def set_background_stylesheet(self, image_path):
        self.setStyleSheet(f"""QMainWindow {{
            background-image: url({image_path});
            background-repeat: no-repeat;
            background-position: center;
        }}""")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def settings(self):
        self.resize_window("./src/20240103_235620.jpg")
        self.center()
        self.setWindowTitle("Settings")
        self.set_background_stylesheet("./src/20240103_235620.jpg")

        self.main_stacked_widget.addWidget(self.settings_window)
        self.main_stacked_widget.setCurrentWidget(self.settings_window)

    def go_back(self):
        self.resize_window()
        self.center()
        self.set_background_stylesheet("./src/nekoxl-24218398-766542997.png")

        self.main_stacked_widget.setCurrentWidget(self.welcome_window)

    def resize_window(
        self, path_to_image="./src/nekoxl-24218398-766542997.png"
    ):
        resolution = self.get_image_resolution(Path(path_to_image))
        if resolution is not None:
            x, y = resolution
            self.resize(x, y)
        else:
            # Handle the case where the image resolution could not be obtained
            # Maybe set the window to a default size or show an error message
            self.go_back()
            return False

    @staticmethod
    def get_image_resolution(image_path):
        if not image_path.exists():
            print(f"File not found: {str(image_path)}")
            return None

        with Image.open(image_path) as img:
            return img.size


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_EnableHighDpiScaling, True
        )

    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_UseHighDpiPixmaps, True
        )

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
