import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLayout
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Домино')
        self.setGeometry(300, 300, 250, 150)
        self.setStyleSheet("background-color: rgb(255,238,140);")
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()




