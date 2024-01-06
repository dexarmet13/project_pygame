from PyQt5.QtGui import QFont, QFontInfo
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QSlider,
    QMessageBox,
    QFrame,
    QGridLayout,
    QComboBox,
)
from PyQt5.QtCore import Qt


class SettingsUI(QWidget):
    def __init__(self):
        self._font = QFont()
        self._font.setPointSize(20)

        super().__init__()
        self.initUI()

    def initUI(self):
        self.frame = QFrame(self)
        self.frame.move(104, 140)
        self.frame.resize(1066, 595)

        self.main_layout = QGridLayout(self)

        label = QLabel("Сложность")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 1, 0, 1, 1)

        self.dificulty_combo_box = QComboBox()
        self.dificulty_combo_box.addItems(["Легкий", "Средний", "Тяжкий"])
        self.main_layout.addWidget(self.dificulty_combo_box, 1, 1, 1, 2)

        label = QLabel("Разрешение")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 2, 0, 1, 1)

        self.game_resolution_combo_box = QComboBox()
        self.game_resolution_combo_box.addItems([
            "2560*1440", "1920*1080", "1280*720"
        ])
        self.main_layout.addWidget(self.game_resolution_combo_box, 2, 1, 1, 2)

        label = QLabel("Качество")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 3, 0, 1, 1)

        self.quality_level_combo_box = QComboBox()
        self.quality_level_combo_box.addItems(["Низкое", "Среднее", "Высокое"])
        self.main_layout.addWidget(self.quality_level_combo_box, 3, 1, 1, 2)

        label = QLabel("Режим")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 4, 0, 1, 1)

        for i, button in enumerate(["Оконный", "Полноэкранный"]):
            button = QPushButton(f"{button}")
            self.set_button_stylesheet(button)
            self.main_layout.addWidget(button, 4, i + 1, 1, 1)

        label = QLabel("Ограничение FPS")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 5, 0, 1, 1)

        self.fps_limit_combo_box = QComboBox()
        self.fps_limit_combo_box.addItems([
            "Без ограничений", "Ограничение 60", "Ограничение 30"
        ])
        self.main_layout.addWidget(self.fps_limit_combo_box, 5, 1, 1, 2)

        label = QLabel("Верт")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 6, 0, 1, 1)

        for i, button in enumerate(["Вкл", "Выкл"]):
            button = QPushButton(f"{button}")
            self.set_button_stylesheet(button)
            self.main_layout.addWidget(button, 6, i + 1, 1, 1)

        self.back_button = QPushButton("Назад")
        self.set_button_stylesheet(self.back_button)
        self.main_layout.addWidget(self.back_button, 7, 0, 1, 1)

        self.accept_button = QPushButton("Применить")
        self.set_button_stylesheet(self.accept_button)
        self.main_layout.addWidget(self.accept_button, 7, 1, 1, 1)

        self.reset = QPushButton("Сбросить")
        self.set_button_stylesheet(self.reset)
        self.main_layout.addWidget(self.reset, 7, 2, 1, 1)

        for i in range(self.main_layout.columnCount()):
            self.main_layout.setColumnStretch(i, 0)

        self.volume_label = QLabel("Громкость")
        self.set_lables_style(self.volume_label)
        self.main_layout.addWidget(self.volume_label, 0, 0, 1, 1)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.main_layout.addWidget(self.volume_slider, 0, 1, 1, 2)

        self.frame.setLayout(self.main_layout)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font_name):
        temp_label = QLabel()
        temp_font = QFont(font_name)
        temp_label.setFont(temp_font)

        font_info = QFontInfo(temp_label._font())

        if font_info.family() == temp_font.family():
            self._font = temp_font
        else:
            QMessageBox.critical(
                self,
                "Ошибка при установке шрифта",
                "Данный шрифт некорректен. Шрифт по умолчанию:"
                f" {font_info.family()}",
            )

    def set_lables_style(self, label):
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setStyleSheet("color: white;")
        label.setFont(self._font)

    def set_button_stylesheet(self, button):
        button.setStyleSheet("color: black;")
        button.setFont(self._font)
