import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

import requests

class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('map.ui', self)

        self.press_delta = 0.005
        self.map_zoom = 10
        self.map_ll = [55.000, 60.000]
        self.map_l = 'map'
        self.map_key = ''
        self.theme = 'light'
        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

        self.refresh_map()

        self.dark.clicked.connect(self.dark_theme)
        self.light.clicked.connect(self.light_theme)

    def dark_theme(self):
        self.theme = 'dark'
        self.refresh_map()

    def light_theme(self):
        self.theme = 'light'
        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if event.key() == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key.Key_Up and self.map_ll[1] <= 89:
            self.map_ll[1] += self.press_delta
        if event.key() == Qt.Key.Key_Down and self.map_ll[1] >= -89:
            self.map_ll[1] -= self.press_delta
        if event.key() == Qt.Key.Key_Left:
            if self.map_ll[0] <= -180:
                self.map_ll[0] = -self.map_ll[0]
            self.map_ll[0] -= self.press_delta
        if event.key() == Qt.Key.Key_Right:
            if self.map_ll[0] >= 180:
                self.map_ll[0] = -self.map_ll[0]
            self.map_ll[0] += self.press_delta
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'l': self.map_l,
            'z': self.map_zoom,
            'theme': self.theme,
            'apikey': self.apikey
        }
        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)

        print(response.content)

        pixmap = QImage()
        pixmap.loadFromData(response.content)
        self.g_map.setPixmap(QPixmap.fromImage(pixmap))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
m = MainWindow()
m.show()
sys.excepthook = except_hook
sys.exit(app.exec())
