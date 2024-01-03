from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)


class WelcomeWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()

        self.button_layout = QHBoxLayout()

        self.settings_button = QPushButton("Настройки")
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-image: url(./src/png-clipart-buttons-buttons.png);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        self.play_button = QPushButton("Играть")
        self.play_button.setStyleSheet("")

        self.about_us_button = QPushButton("Создатели")
        self.about_us_button.setStyleSheet("")

        self.add_buttons_to_layout()

        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def add_buttons_to_layout(self):
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.settings_button)
        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.about_us_button)
        self.button_layout.addStretch(1)
