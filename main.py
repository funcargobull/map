from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import sys
from load_map import *


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('design.ui', self)
        for i in self.mode_group.buttons():
            i.setFocusPolicy(Qt.ClickFocus)
        self.to_search.setFocusPolicy(Qt.ClickFocus)

        self.start_spn = 12
        self.start_index = False
        self.start_mode = "map"

        self.longitude = None
        self.lattitude = None
        self.address = None

        self.search_btn.clicked.connect(
            lambda: self.search_button_click(self.get_user_search()))

        self.clear_btn.clicked.connect(self.clear_)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            try:
                if self.start_spn + 1 <= 21:
                    self.start_spn += 1
                    self.search_button_click(self.get_user_search())
            except KeyError:
                pass
        elif e.key() == Qt.Key_PageDown:
            try:
                if self.start_spn - 1 >= 0:
                    self.start_spn -= 1
                    self.search_button_click(self.get_user_search())
            except KeyError:
                pass
        elif e.key() in [Qt.Key_Up, Qt.Key_Left, Qt.Key_Right, Qt.Key_Down]:
            try:
                if e.key() == Qt.Key_Up:
                    if self.lattitude + 0.5 / self.start_spn <= 180:
                        self.lattitude += 0.5 / self.start_spn
                elif e.key() == Qt.Key_Down:
                    if self.lattitude - 0.5 / self.start_spn >= 0:
                        self.lattitude -= 0.5 / self.start_spn
                elif e.key() == Qt.Key_Left:
                    if self.longitude - 0.5 / self.start_spn >= 0:
                        self.longitude -= 0.5 / self.start_spn
                else:
                    if self.longitude + 0.5 / self.start_spn <= 180:
                        self.longitude += 0.5 / self.start_spn
                image = load_map(self.longitude, self.lattitude,
                                 self.start_spn, self.start_mode)
                self.show_image(image, self.address)
            except KeyError:
                pass
            except TypeError:
                pass

    def get_user_search(self):
        return self.to_search.text()

    def search_button_click(self, toponym):
        for i in self.mode_group.buttons():
            if i.text() == "Схема" and i.isChecked():
                self.start_mode = "map"
            elif i.text() == "Спутник" and i.isChecked():
                self.start_mode = "sat"
            elif i.text() == "Гибрид" and i.isChecked():
                self.start_mode = "skl"

        toponym_longitude, toponym_lattitude, address = get_coords_and_address(
            toponym)
        self.longitude = float(toponym_longitude)
        self.lattitude = float(toponym_lattitude)

        self.address = address
        image = load_map(self.longitude, self.lattitude,
                         self.start_spn, self.start_mode)
        self.show_image(image, address)

    def show_image(self, image, address):
        img = QImage()
        img.loadFromData(image)
        self.pixmap_label.setPixmap(QPixmap.fromImage(img))
        self.statusBar().showMessage(address)

    def clear_(self):
        self.pixmap_label.clear()
        self.statusBar().showMessage("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
