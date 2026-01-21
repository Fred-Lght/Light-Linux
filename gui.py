import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QWidget, QVBoxLayout, QLabel, QStackedWidget
)
import subprocess
import psutil

ping = ["ping", "-c", "2", "google.com"]


def run_cmd():
    try:
        rls = subprocess.run(ping, capture_output=True, text=True, check=False)
        return rls.returncode
    except Exception:
        return -1


def get_disks_info():
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        disks.append({
            "device": part.device,
            "mount": part.mountpoint,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        })
    return disks


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Installer")
        self.resize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # ---------- Page 1 ----------
        self.page1 = QWidget()
        layout1 = QVBoxLayout()

        self.label1 = QLabel("Приветствуем вас в мастере установщике")
        self.button1 = QPushButton("Install?")

        layout1.addWidget(self.label1)
        layout1.addWidget(self.button1)
        self.page1.setLayout(layout1)

        self.button1.clicked.connect(self.check_and_go)

        # ---------- Page 2 ----------
        self.page2 = QWidget()
        self.layout2 = QVBoxLayout()

        self.label2 = QLabel("Информация о дисках:")
        self.disk_label = QLabel("")
        self.disk_label.setWordWrap(True)

        self.button_back = QPushButton("Назад")

        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.disk_label)
        self.layout2.addWidget(self.button_back)

        self.page2.setLayout(self.layout2)

        self.button_back.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page1)
        )

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def check_and_go(self):
        rc = run_cmd()

        if rc == 0:
            self.label1.setText("Интернет есть")
        else:
            self.label1.setText("Нет интернета")

        self.show_disks()
        self.stack.setCurrentWidget(self.page2)

    def show_disks(self):
        disks = get_disks_info()
        text = ""

        for d in disks:
            text += (
                f"Диск: {d['device']}\n"
                f"Монтирование: {d['mount']}\n"
                f"Всего: {d['total'] // (1024**3)} GB\n"
                f"Занято: {d['used'] // (1024**3)} GB\n"
                f"Свободно: {d['free'] // (1024**3)} GB\n\n"
            )

        self.disk_label.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

