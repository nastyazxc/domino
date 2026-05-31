import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DominoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.init_main_menu()

    def initUI(self):
        self.setWindowTitle('Домино')
        self.setStyleSheet("QMainWindow { background-color: rgb(255,238,140); }")
        self.setGeometry(300, 300, 800, 600)

    def init_main_menu(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("ДОМИНО")
        title.setFont(QFont("Verdana", 72, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 40px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        for txt in ["ИГРАТЬ", "ПРАВИЛА", "ВЫХОД"]:
            btn = QPushButton(txt)
            btn.setFixedSize(400, 80)
            btn.setFont(QFont("Arial", 22))
            btn.setStyleSheet("background-color: #fdfdfd; border: 1px solid #333; border-radius: 10px; color: #000;")
            
            if txt == "ИГРАТЬ":
                btn.clicked.connect(self.start_new_game)  # заглушка
            elif txt == "ПРАВИЛА":
                btn.clicked.connect(lambda: self.stacked.setCurrentIndex(1))  # заглушка
            else:
                btn.clicked.connect(self.close)
            
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(15)
        
        self.stacked.addWidget(widget)

    def start_new_game(self):
        # Заглушка: просто переключаем на game_screen (пока не реализован)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DominoApp()
    ex.showMaximized()
    sys.exit(app.exec())


