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
        self.init_rules_screen()

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
                btn.clicked.connect(self.start_new_game)
            elif txt == "ПРАВИЛА":
                btn.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
            else:
                btn.clicked.connect(self.close)
            
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(15)
        
        self.stacked.addWidget(widget)

    def init_rules_screen(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: rgb(255,238,140);")
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("ПРАВИЛА ИГРЫ")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: #000; margin-bottom: 40px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        rules_text = QLabel(
            "1. Используется 28 костяшек (от 0-0 до 6-6)\n\n"
            "2. Каждому игроку раздается по 7 костяшек\n\n"
            "3. Первый ход делает игрок с дублем 1-1\n"
            "   Если его нет - с наибольшим дублем\n\n"
            "4. Цель игры - первым выложить все свои костяшки\n\n"
            "5. Если нет подходящей костяшки - берите из базара\n\n"
            "6. 'Рыба' - если никто не может ходить,\n"
            "   побеждает игрок с меньшей суммой очков\n\n"
            "7. Игра заканчивается, когда один из игроков\n"
            "   выложил все костяшки или наступила 'рыба'"
        )
        rules_text.setFont(QFont("Arial", 16))
        rules_text.setStyleSheet("color: #000; margin-bottom: 30px;")
        rules_text.setWordWrap(True)
        rules_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn = QPushButton("НАЗАД")
        btn.setFixedSize(200, 60)
        btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #fdfdfd;
                border: 2px solid #333;
                border-radius: 10px;
                color: #000;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(rules_text)
        layout.addSpacing(30)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.stacked.addWidget(widget)

    def start_new_game(self):
        # Заглушка: пока просто переключаем (игровой экран еще не готов)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DominoApp()
    ex.showMaximized()
    sys.exit(app.exec())