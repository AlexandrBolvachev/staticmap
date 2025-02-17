# requests.exceptions.SSLError: HTTPSConnectionPool(host='static-maps.yandex.ru', port=443): Max retries exceeded with url: /1.x/?ll=37.615%2C55.752&l=map&z=10 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')))

import sys
from PyQt6 import uic
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
        self.map_ll = [37.615, 55.752]
        self.map_l = 'map'
        self.map_key = ''
        self.refresh_map()


    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'l': self.map_l,
            'z': self.map_zoom
        }
        map_api_server = "https://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

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
