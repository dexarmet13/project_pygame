from PyQt5.QtGui import QFont, QFontInfo
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QSlider,
    QVBoxLayout,
    QMessageBox,
    QFrame,
    QCheckBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt


class SettingsUI(QWidget):
    def __init__(self):
        self._font = QFont()
        self._font.setPointSize(20)

        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        self.frame = QFrame(self)
        self.frame.move(104, 140)
        self.frame.resize(1066, 595)

        self.back_button = QPushButton("Назад")
        self.back_button.setStyleSheet("color: black;")
        self.back_button.setFont(self.font)
        self.main_layout.addWidget(self.back_button)

        self.create_sound_level()
        self.create_dificulty_level_buttons()
        self.create_game_resolution()
        self.create_quality_level_buttons()
        self.create_window_mode_buttons()
        self.create_fps_limits_buttons()
        self.create_vertical_sync()

        self.frame.setLayout(self.main_layout)

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

    def set_lables_style(self, label):
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setStyleSheet("color: white;")
        label.setFont(self.font)

    def create_sound_level(self):
        layout = QHBoxLayout()

        self.volume_label = QLabel("Громкость")
        self.set_lables_style(self.volume_label)
        layout.addWidget(self.volume_label, 0)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.volume_changed)
        layout.addWidget(self.volume_slider, 1)

        self.sound_level = QLabel("50%")
        self.sound_level.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.sound_level.setStyleSheet("color: white;")
        self.sound_level.setFont(self.font)
        layout.addWidget(self.sound_level, 0)

        self.main_layout.addLayout(layout, 0)

    def volume_changed(self):
        self.sound_level.setText(f"{self.volume_slider.value()}%")

    def create_dificulty_level_buttons(self):
        layout = QHBoxLayout()

        label = QLabel("Сложность")
        self.set_lables_style(label)
        layout.addWidget(label)

        for i, difficulty in enumerate(["Легкий", "Средний", "Тяжкий"]):
            button = QPushButton(f"{difficulty}")
            button.setStyleSheet("color: black;")
            button.setFont(self.font)

            layout.addWidget(button)

        self.main_layout.addLayout(layout, 1)

    def create_game_resolution(self):
        layout = QHBoxLayout()

        label = QLabel("Разрешение")
        self.set_lables_style(label)
        layout.addWidget(label)

        for i, resolution in enumerate(["2560*1440", "1920*1080", "1280*720"]):
            button = QPushButton(f"{resolution}")
            button.setStyleSheet("color: black;")
            button.setFont(self.font)

            layout.addWidget(button)

        self.main_layout.addLayout(layout, 2)

    def create_quality_level_buttons(self):
        layout = QHBoxLayout()

        label = QLabel("Качество")
        self.set_lables_style(label)
        layout.addWidget(label, 1)

        for quality in ["Низкое", "Среднее", "Высокое"]:
            button = QPushButton(f"{quality}")
            button.setStyleSheet("color: black;")
            button.setFont(self.font)
            layout.addWidget(button, 1)

        self.main_layout.addLayout(layout, 3)

    def create_window_mode_buttons(self):
        layout = QHBoxLayout()

        label = QLabel("Режим")
        self.set_lables_style(label)
        layout.addWidget(label, 1)

        for i, window_mode in enumerate(["Оконный", "Полноэкранный"]):
            button = QPushButton(f"{window_mode}")
            button.setStyleSheet("color: black;")
            button.setFont(self.font)

            layout.addWidget(button, 2)

        self.main_layout.addLayout(layout, 4)

    def create_fps_limits_buttons(self):
        layout = QHBoxLayout()

        label = QLabel("Ограничение FPS")
        self.set_lables_style(label)
        layout.addWidget(label)

        for i, fps_limit in enumerate([
            "Без ограничений", "Ограничение 60", "Ограничение 30"
        ]):
            button = QPushButton(f"{fps_limit}")
            button.setStyleSheet("color: black;")
            button.setFont(self.font)

            layout.addWidget(button)

        self.main_layout.addLayout(layout, 5)

    def create_vertical_sync(self):
        layout = QHBoxLayout()

        label = QLabel("Вертикальная синхронизация")
        self.set_lables_style(label)
        layout.addWidget(label, 1)

        self.checkbox = QCheckBox("Вкл / Выкл", self)
        layout.addWidget(self.checkbox, 1)

        self.main_layout.addLayout(layout, 6)
