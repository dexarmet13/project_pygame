import json
from pathlib import Path
from PyQt5.QtGui import QFont, QFontInfo, QPalette, QColor
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

        self._dict_settings = {}

        super().__init__()
        self.initUI()

    def initUI(self):
        self.frame = QFrame(self)
        self.frame.move(104, 140)
        self.frame.resize(1066, 595)

        self.main_layout = QGridLayout(self.frame)

        label = QLabel("Уровень сложности")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 1, 0, 1, 1)

        self.dificulty_combo_box = QComboBox()
        self.set_combo_box_stylesheet(self.dificulty_combo_box)
        self.dificulty_combo_box.addItems(["Легкий", "Средний", "Тяжелый"])
        self.main_layout.addWidget(self.dificulty_combo_box, 1, 1, 1, 2)

        label = QLabel("Разрешение экрана")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 2, 0, 1, 1)

        self.game_resolution_combo_box = QComboBox()
        self.set_combo_box_stylesheet(self.game_resolution_combo_box)
        self.game_resolution_combo_box.addItems([
            "2560*1440", "1920*1080", "1280*720"
        ])
        self.main_layout.addWidget(self.game_resolution_combo_box, 2, 1, 1, 2)

        label = QLabel("Качество текстур")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 3, 0, 1, 1)

        self.quality_level_combo_box = QComboBox()
        self.set_combo_box_stylesheet(self.quality_level_combo_box)
        self.quality_level_combo_box.addItems(["Низкое", "Среднее", "Высокое"])
        self.main_layout.addWidget(self.quality_level_combo_box, 3, 1, 1, 2)

        label = QLabel("Режим отображения")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 4, 0, 1, 1)

        window_mode_button = QPushButton("Оконный")
        self.create_button(window_mode_button, 4, 1)

        fullscreen_mode_button = QPushButton("Полноэкранный")
        self.create_button(fullscreen_mode_button, 4, 2)

        label = QLabel("Ограничение по FPS")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 5, 0, 1, 1)

        self.fps_limit_combo_box = QComboBox()
        self.set_combo_box_stylesheet(self.fps_limit_combo_box)
        self.fps_limit_combo_box.addItems([
            "Без ограничений", "Ограничение 60", "Ограничение 30"
        ])
        self.main_layout.addWidget(self.fps_limit_combo_box, 5, 1, 1, 2)

        label = QLabel("Вертикальная синхронизация")
        self.set_lables_style(label)
        self.main_layout.addWidget(label, 6, 0, 1, 1)

        vert_sync_on_button = QPushButton("Включить")
        self.create_button(vert_sync_on_button, 6, 1)

        vert_sync_off_button = QPushButton("Выключить")
        self.create_button(vert_sync_off_button, 6, 2)

        self.back_button = QPushButton("Назад")
        self.set_button_stylesheet(self.back_button)
        self.main_layout.addWidget(self.back_button, 7, 0, 1, 1)

        self.accept_button = QPushButton("Применить")
        self.accept_button.clicked.connect(self.accept_settings)
        self.set_button_stylesheet(self.accept_button)
        self.main_layout.addWidget(self.accept_button, 7, 1, 1, 1)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_settings)
        self.set_button_stylesheet(self.reset_button)
        self.main_layout.addWidget(self.reset_button, 7, 2, 1, 1)

        for i in range(self.main_layout.columnCount()):
            self.main_layout.setColumnStretch(i, 0)

        self.volume_label = QLabel("Громкость звука")
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

    @property
    def dict_settings(self):
        return self._dict_settings

    @dict_settings.setter
    def dict_settings(self, dict_settings):
        self._dict_settings = dict_settings

    def set_lables_style(self, label):
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setStyleSheet("color: white;")
        label.setFont(self._font)

    def set_button_stylesheet(self, button):
        button.setStyleSheet("color: black;")
        button.setFont(self._font)

    def set_combo_box_stylesheet(self, combo_box):
        combo_box.setStyleSheet("color: black;")
        combo_box.setFont(self._font)

    @staticmethod
    def set_button_color(button, color):
        palette = button.palette()
        palette.setColor(QPalette.Button, QColor(color))

        button.setPalette(palette)
        button.setAutoFillBackground(True)

    def create_button(self, button, y, x):
        button.clicked.connect(lambda: self.get_button_statement(button, y))
        self.set_button_stylesheet(button)
        self.main_layout.addWidget(button, y, x, 1, 1)

    def get_button_statement(self, button, y):
        for column in range(self.main_layout.columnCount()):
            item = self.main_layout.itemAtPosition(y, column)
            widget = item.widget()
            if column:
                current_color = widget.palette().color(QPalette.Button).name()
                if current_color == "#008000":
                    self.set_button_color(widget, "white")
        self.set_button_color(button, "green")

    def accept_settings(self):
        for row in range(self.main_layout.rowCount()):
            for column in range(self.main_layout.columnCount()):
                item = self.main_layout.itemAtPosition(row, column)
                if item is not None:
                    widget = item.widget()
                    if column == 0:
                        key = widget.text()
                    elif isinstance(widget, QSlider):
                        self._dict_settings[key] = widget.value()
                    elif isinstance(widget, QPushButton):
                        current_color = (
                            widget.palette().color(QPalette.Button).name()
                        )
                        if current_color == "#008000":
                            if row == 6:
                                self._dict_settings[key] = (
                                    widget.text() == "Включить"
                                )
                            else:
                                self._dict_settings[key] = widget.text()
                    elif isinstance(widget, QComboBox):
                        if row == 2:
                            values = widget.currentText().split("*")
                            self._dict_settings[key] = (
                                int(values[0]),
                                int(values[1]),
                            )
                        elif row == 5:
                            text = widget.currentText()
                            self._dict_settings[key] = (
                                None
                                if text == "Без ограничений"
                                else int(text[-2:])
                            )
                        else:
                            self._dict_settings[key] = widget.currentText()

        if len(self._dict_settings) < self.main_layout.rowCount() - 1:
            QMessageBox.critical(
                self, "Ошибка", "Все настройки должны быть заполнены"
            )
            return False

        self.create_json_file()

    def create_json_file(self):
        directory = Path("user_data")
        file_path = directory / "settings.json"

        directory.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as json_file:
            json.dump(
                self._dict_settings, json_file, ensure_ascii=False, indent=4
            )
        QMessageBox.information(self, "Готово", "Настройки сохранены")

    def reset_settings(self):
        dict_settings = {
            "Громкость звука": 50,
            "Уровень сложности": "Средний",
            "Разрешение экрана": [2560, 1440],
            "Качество текстур": "Среднее",
            "Режим отображения": "Оконный",
            "Ограничение по FPS": 60,
            "Вертикальная синхронизация": False,
        }
        self.set_settings(dict_settings)

    def set_settings(
        self, dict_settings=json.load(open("user_data/settings.json", "r"))
    ):
        print(dict_settings)
        self._dict_settings = dict_settings
        for row in range(self.main_layout.rowCount()):
            for column in range(self.main_layout.columnCount()):
                item = self.main_layout.itemAtPosition(row, column)
                widget = item.widget()
                if row == self.main_layout.rowCount() - 1:
                    continue
                if column == 0:
                    key = widget.text()
                elif isinstance(widget, QSlider):
                    widget.setValue(self._dict_settings[key])
                elif isinstance(widget, QPushButton):
                    if row == 6:
                        if (
                            widget.text() == "Включить"
                            and self._dict_settings[key]
                        ) or (
                            widget.text() == "Выключить"
                            and not self._dict_settings[key]
                        ):
                            self.set_button_color(widget, "green")
                        else:
                            self.set_button_color(widget, "white")
                    elif widget.text() == self._dict_settings[key]:
                        self.set_button_color(widget, "green")
                    else:
                        self.set_button_color(widget, "white")
                else:
                    if row == 2:
                        widget.setCurrentText(
                            f"{self._dict_settings[key][0]}*{self._dict_settings[key][1]}"
                        )
                        print(self._dict_settings[key])
                    elif row == 5:
                        if self._dict_settings[key] is None:
                            widget.setCurrentText("Без ограничений")
                        else:
                            widget.setCurrentText(
                                f"Ограничение {self._dict_settings[key]}"
                            )
                    else:
                        widget.setCurrentText(self._dict_settings[key])
