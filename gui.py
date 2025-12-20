import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
import subprocess

ping = ["ping", "-c", "4", "google.com"]

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

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        self.label = QLabel("Приветсвуем вас в мастере установщике для *place holder*")
        self.button = QPushButton("Install?")

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.change_text)

        central.setLayout(layout)

        self.setWindowTitle('Installer')
        self.resize(1920, 1080)

    def change_text(self):
        global result
        result = run_cmd()

        if result["returncode"] == 0:
            self.label.setText("Установка началась (нет)")    
        else:
            self.label.setText("No internet (loch)")

        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
