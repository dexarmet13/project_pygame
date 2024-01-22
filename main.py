import sys
from PyQt5.QtGui import QPixmap, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QDesktopWidget,
    QMessageBox,
    QFileDialog,
)
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt
from welcome_window_ui import WelcomeWindowUI
from settings_ui import SettingsUI
from platformer import GameWindow
from map_editor_window import MapEditorWindow


class MainWindow(QMainWindow):
    def __init__(self):
        self.app = app

        self._images = {
            "main_window_background": QPixmap(
                "materials/backgrounds/main_background.png"
            ),
            "settings_window_background": QPixmap(
                "materials/backgrounds/settings_background.jpg"
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
            self.welcome_window.settings_button,
            "materials/button_bg/buttons_texture.png",
        )
        self.welcome_window.play_button.clicked.connect(self.play)
        self.set_button_stylesheet(
            self.welcome_window.play_button,
            "materials/button_bg/buttons_texture.png",
        )
        self.welcome_window.map_editor.clicked.connect(self.edit_map)
        self.set_button_stylesheet(
            self.welcome_window.map_editor,
            "materials/button_bg/buttons_texture.png",
        )

        self.main_stacked_widget.addWidget(self.welcome_window)
        self.main_stacked_widget.setCurrentWidget(self.welcome_window)

        self.settings_window.back_button.clicked.connect(self.go_back)

        self.main_stacked_widget.addWidget(self.settings_window)

        self.textures = None

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
        self.screen = QApplication.primaryScreen()
        self.screen_size = self.screen.size()

        pixmap = self._images.get(image_key)
        if pixmap:
            pixmap_size = pixmap.size()
            if (
                pixmap_size.width() > self.screen_size.width()
                or pixmap_size.height() > self.screen_size.height()
            ):
                pixmap = pixmap.scaled(
                    self.screen_size.width(),
                    self.screen_size.height(),
                    QtCore.Qt.KeepAspectRatio,
                )

            palette = self.palette()
            palette.setBrush(self.backgroundRole(), QBrush(pixmap))
            self.setPalette(palette)
        return False

    def set_button_stylesheet(self, button, image_path):
        button.setFixedSize(QSize(190, 126))
        button.setFont(self.settings_window.font)
        button.setStyleSheet(
            f"""border-image: url("{image_path}"); color: white;"""
        )

    def resize_window(self, image_key):
        pixmap = self._images.get(image_key)
        if pixmap:
            pixmap_size = pixmap.size()
            if (
                pixmap_size.width() > self.screen_size.width()
                or pixmap_size.height() > self.screen_size.height()
            ):
                self.resize(
                    self.screen_size.width(), self.screen_size.height()
                )
            else:
                self.resize(pixmap_size.width(), pixmap_size.height())
            return True
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
        game_windwow = GameWindow()
        game_windwow.main()
        self.show()

    def edit_map(self):
        self.hide()

        game_window = MapEditorWindow(
            (self.screen_size.width(), self.screen_size.height())
        )
        game_window.main()

        self.show()
        self.show_popup(game_window)

    def show_popup(self, game_window):
        reply = QMessageBox.question(
            self,
            "Сообщение",
            "Сохранить карту?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        textures = game_window.texture_places
        if reply == QMessageBox.Yes and textures is not None:
            self.textures = game_window.save_textures()
            print(self.textures)
            self.show_save_file_dialog()

    def show_save_file_dialog(self):
        options = QFileDialog.Options()

        defaultFileName = "Untitled_map.txt"
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл как...",
            defaultFileName,
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if fileName:
            print(f"Выбранный файл для сохранения: {fileName}")
            # Здесь код для сохранения данных в выбранный файл


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
