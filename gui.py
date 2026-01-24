# gui.py
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


import system


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("install.ui", self)

        # сигналы
        self.pushButton.clicked.connect(self.on_install)


    def on_install(self):
        ok = system.check_internet()

        if not ok:
            self.welcomeLabel.setText("Нет интернета")
            return

        self.fill_disks()
        self.stackedWidget.setCurrentIndex(1)

    def fill_disks(self):
        disks = system.get_disks()
        self.disksTable.setRowCount(len(disks))
        self.disksTable.setColumnCount(4)
        self.disksTable.setHorizontalHeaderLabels(
            ["Диск", "Mount", "Всего (GB)", "Свободно (GB)"]
        )

        for row, d in enumerate(disks):
            self.disksTable.setItem(row, 0, QTableWidgetItem(d["device"]))
            self.disksTable.setItem(row, 1, QTableWidgetItem(d["mount"]))
            self.disksTable.setItem(row, 2, QTableWidgetItem(str(d["total"] // 1024**3)))
            self.disksTable.setItem(row, 3, QTableWidgetItem(str(d["free"] // 1024**3)))

    def on_back(self):
        self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

