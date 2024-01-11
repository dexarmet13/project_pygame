import sys
from PyQt5.QtGui import QPixmap, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QDesktopWidget,
    QMessageBox,
)
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt
from welcome_window_ui import WelcomeWindowUI
from settings_ui import SettingsUI
from platformer import main


class MainWindow(QMainWindow):
    def __init__(self):
        self._images = {
            "main_window_background": QPixmap(
                "src/main_window_background.png"
            ),
            "settings_window_background": QPixmap(
                "src/settings_window_background.jpg"
            ),
        }

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Welcome Window")
        self.set_background_pixmap("main_window_background")
        self.resize_window("main_window_background")

        self.center()

        self.main_stacked_widget = QStackedWidget()
        self.setCentralWidget(self.main_stacked_widget)

        self.welcome_window = WelcomeWindowUI()
        self.settings_window = SettingsUI()

        self.welcome_window.settings_button.clicked.connect(self.settings)
        self.set_button_stylesheet(
            self.welcome_window.settings_button, "src/buttons_texture.png"
        )
        self.welcome_window.play_button.clicked.connect(self.play)
        self.set_button_stylesheet(
            self.welcome_window.play_button, "src/play_button_texture.png"
        )
        self.set_button_stylesheet(
            self.welcome_window.about_us_button, "src/buttons_texture.png"
        )

        self.main_stacked_widget.addWidget(self.welcome_window)
        self.main_stacked_widget.setCurrentWidget(self.welcome_window)

        self.settings_window.back_button.clicked.connect(self.go_back)

        self.main_stacked_widget.addWidget(self.settings_window)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showDialog()
        elif event.key() == Qt.Key_Return:
            self.play()

    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Закрыть приложение?")
        msgBox.setWindowTitle("Подтверждение выхода")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_background_pixmap(self, image_key):
        pixmap = self._images.get(image_key)
        if pixmap:
            screen = QApplication.primaryScreen()
            screen_size = screen.size()
            pixmap_size = pixmap.size()
            if (
                pixmap_size.width() > screen_size.width()
                or pixmap_size.height() > screen_size.height()
            ):
                pixmap = pixmap.scaled(
                    screen_size.width(),
                    screen_size.height(),
                    QtCore.Qt.KeepAspectRatio,
                )

            palette = self.palette()
            palette.setBrush(self.backgroundRole(), QBrush(pixmap))
            self.setPalette(palette)
        else:
            print(f"Image key not found: {image_key}")

    def set_button_stylesheet(self, button, image_path):
        button.setFixedSize(QSize(190, 126))
        button.setFont(self.settings_window.font)
        button.setStyleSheet(
            f"""border-image: url("{image_path}"); color: white;"""
        )

    def resize_window(self, image_key):
        pixmap = self._images.get(image_key)
        if pixmap:
            screen = QApplication.primaryScreen()
            screen_size = screen.size()
            pixmap_size = pixmap.size()
            if (
                pixmap_size.width() > screen_size.width()
                or pixmap_size.height() > screen_size.height()
            ):
                self.resize(screen_size.width(), screen_size.height())
            else:
                self.resize(pixmap_size.width(), pixmap_size.height())
            return True
        print(f"Image key not found: {image_key}")
        return False

    def settings(self):
        self.set_background_pixmap("settings_window_background")
        if not self.resize_window("settings_window_background"):
            return False
        self.center()
        self.setWindowTitle("Settings")

        self.main_stacked_widget.setCurrentWidget(self.settings_window)

    def go_back(self):
        self.set_background_pixmap("main_window_background")
        self.resize_window("main_window_background")
        self.center()

        self.main_stacked_widget.setCurrentWidget(self.welcome_window)

    def play(self):
        self.hide()
        main()
        self.show()


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
