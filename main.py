import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# --- ЛОГИКА ИГРЫ ---
class DominoLogic:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.deck = [(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(self.deck)
        self.hands = {1: self.deck[:7], 2: self.deck[7:14]}
        self.bazaar = self.deck[14:]
        self.board = []
        self.current_player = self.determine_first_player()

    def determine_first_player(self):
        for p in [1, 2]:
            if (1, 1) in self.hands[p]:
                return p
        best_double = -1
        best_player = 1
        for p in [1, 2]:
            for tile in self.hands[p]:
                if tile[0] == tile[1] and tile[0] > best_double:
                    best_double = tile[0]
                    best_player = p
        if best_double != -1:
            return best_player
        max_sum = -1
        for p in [1, 2]:
            for tile in self.hands[p]:
                if sum(tile) > max_sum:
                    max_sum = sum(tile)
                    best_player = p
        return best_player

    def is_valid_move(self, tile):
        if not self.board:
            return True
        l, r = self.board[0][0], self.board[-1][1]
        return tile[0] in (l, r) or tile[1] in (l, r)

    def make_move(self, tile, player):
        if not self.board:
            self.board.append(tile)
        else:
            l, r = self.board[0][0], self.board[-1][1]
            if tile[1] == l:
                self.board.insert(0, tile)
            elif tile[0] == l:
                self.board.insert(0, (tile[1], tile[0]))
            elif tile[0] == r:
                self.board.append(tile)
            elif tile[1] == r:
                self.board.append((tile[1], tile[0]))
        self.hands[player].remove(tile)
        self.current_player = 2 if player == 1 else 1

    def calculate_score(self, player):
        return sum(sum(tile) for tile in self.hands[player])


# --- ИНТЕРФЕЙС ---
class DominoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.logic = DominoLogic()
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self.init_main_menu()
        self.init_rules_screen()
        self.init_game_screen()

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

    def init_game_screen(self):
        self.game_widget = QWidget()
        main_l = QVBoxLayout(self.game_widget)
        info_l = QHBoxLayout()

        btn_home = QPushButton("ВЕРНУТЬСЯ В МЕНЮ") 
        btn_home.setFixedSize(250, 60)
        btn_home.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_home.setStyleSheet("""
            background-color: #fdfdfd; 
            border: 2px solid #333; 
            border-radius: 10px; 
            color: #000;
        """)
        btn_home.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        
        self.opp_lbl = QLabel()
        self.baz_lbl = QLabel()
        for lbl in [self.opp_lbl, self.baz_lbl]:
            lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #333;")
        info_l.addWidget(btn_home)
        info_l.addSpacing(20)
        info_l.addWidget(self.opp_lbl)
        info_l.addStretch()
        info_l.addWidget(self.baz_lbl)
        main_l.addLayout(info_l)

        self.board_area = QWidget()
        self.board_l = QHBoxLayout(self.board_area)
        self.board_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_l.addWidget(self.board_area, 1)

        self.turn_lbl = QLabel()
        self.turn_lbl.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.turn_lbl.setStyleSheet("color: #d35400;")
        main_l.addWidget(self.turn_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.hand_area = QWidget()
        self.hand_l = QHBoxLayout(self.hand_area)
        self.hand_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_l.addWidget(self.hand_area)

        ctrl_l = QHBoxLayout()
        btn_baz = QPushButton("ВЗЯТЬ ИЗ БАЗАРА")
        btn_sur = QPushButton("СДАТЬСЯ")
        for b in [btn_baz, btn_sur]:
            b.setFixedSize(250, 60)
            b.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            b.setStyleSheet("background-color: #c0392b; color: white; border-radius: 5px;")
        
        btn_baz.clicked.connect(self.draw_bazaar)
        btn_sur.clicked.connect(self.surrender_action)
        ctrl_l.addStretch()
        ctrl_l.addWidget(btn_baz)
        ctrl_l.addWidget(btn_sur)
        ctrl_l.addStretch()
        main_l.addLayout(ctrl_l)
        self.stacked.addWidget(self.game_widget)

    def start_new_game(self):
        self.logic.reset_game()
        self.stacked.setCurrentIndex(2)

    def draw_bazaar(self):
        # Заглушка
        pass

    def surrender_action(self):
        # Заглушка
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DominoApp()
    ex.showMaximized()
    sys.exit(app.exec())