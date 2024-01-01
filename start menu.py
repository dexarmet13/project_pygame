import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize


class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        oImage = QImage("background2.PNG")
        sImage = oImage.scaled(QSize(1000, 750))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.setWindowTitle('Initial Window')
        self.setGeometry(100, 100, 1000, 750)
        self.setFixedSize(1000, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        button_layout = QHBoxLayout()

        label = QLabel()
        pixmap = QPixmap('image.jpg')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        button1 = QPushButton('Button 1')
        # button1.setIcon(QPixmap('button1.png'))
        # button1.setIconSize(QSize(100, 100))

        button2 = QPushButton('Button 2')
        # button2.setIcon(QPixmap('button2.png'))
        # button2.setIconSize(QSize(100, 100))

        button3 = QPushButton('Button 3')
        # button3.setIcon(QPixmap('button3.png'))
        # button3.setIconSize(QSize(100, 100))

        button_layout.addStretch(1)
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InitialWindow()
    window.show()
    sys.exit(app.exec_())
