import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QStackedWidget
import subprocess

ping = ["ping", "-c", "2", "google.com"]

def run_cmd():
    try:
        rls = subprocess.run(ping, capture_output=True, text=True, check=False)
        return {
            "stdout": rls.stdout.strip(),
            "stderr": rls.stderr.strip(),
            "returncode": rls.returncode
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1 }


global result
result = run_cmd()
print("Out", result["stdout"])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Installer')
        self.resize(800, 600)

        # 
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # страница
        self.page1 = QWidget()
        layout1 = QVBoxLayout()

        self.label1 = QLabel("Приветсвуем вас в мастере установщике для *place holder*")
        self.button1 = QPushButton("Install?")

        layout1.addWidget(self.label1)
        layout1.addWidget(self.button1)
        self.page1.setLayout(layout1)

        self.button1.clicked.connect(self.check_internet_and_go_next)

        # страница 2
        self.page2 = QWidget()
        layout2 = QVBoxLayout()
        self.label2 = QLabel("Здесь будет процесс установки...")
        self.button_back = QPushButton("Назад")
        layout2.addWidget(self.label2)
        layout2.addWidget(self.button_back)
        self.page2.setLayout(layout2)

        self.button_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.page1))

        # добавляем страницус
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def check_internet_and_go_next(self):
        global result
        result = run_cmd()

        if result["returncode"] == 0:
            self.label1.setText("Установка началась (нет)")    
        else:
            self.label1.setText("No internet (loch)")

        # переключаемся на вторую страницу
        self.stack.setCurrentWidget(self.page2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
