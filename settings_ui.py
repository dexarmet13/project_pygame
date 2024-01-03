from PyQt5.QtGui import QFont, QFontInfo
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QSlider,
    QGridLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt


class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QGridLayout(self)

        self._font = QFont()
        self._font.setPointSize(20)

        self.back_button = QPushButton("Назад")
        self.main_layout.addWidget(self.back_button, 0, 0, 1, 4)

        self.create_labels()

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.volume_changed)
        self.main_layout.addWidget(self.volume_slider, 2, 1, 1, 2)

        self.sound_level = QLabel("50%")
        self.sound_level.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.sound_level.setStyleSheet("color: white;")
        self.sound_level.setFont(self.font)
        self.main_layout.addWidget(self.sound_level, 2, 3, 1, 1)

        self.setLayout(self.main_layout)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font_name):
        temp_label = QLabel()
        temp_font = QFont(font_name)
        temp_label.setFont(temp_font)

        font_info = QFontInfo(temp_label.font())

        if font_info.family() == temp_font.family():
            self._font = temp_font
        else:
            QMessageBox.critical(
                self,
                "Ошибка при установке шрифта",
                "Данный шрифт некорректен. Шрифт по умолчанию:"
                f" {font_info.family()}",
            )

    def create_labels(self):
        labels = [
            "Звук",
            "Сложность игры",
            "Разрешение",
            "Качество текстур",
            "Режим отображения",
            "Ограничение частоты кадров",
            "Вертикальная синхронизация",
        ]

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            label.setFont(self.font)

            self.main_layout.addWidget(label, i + 2, 0, 1, 1)

    def volume_changed(self):
        self.sound_level.setText(f"{self.volume_slider.value()}%")
