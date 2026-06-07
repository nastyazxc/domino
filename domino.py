import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QMessageBox, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# ЛОГИКА ИГРЫ
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
            if (1, 1) in self.hands[p]: return p
        best_double = -1
        best_player = 1
        for p in [1, 2]:
            for tile in self.hands[p]:
                if tile[0] == tile[1] and tile[0] > best_double:
                    best_double = tile[0]
                    best_player = p
        if best_double != -1: return best_player
        max_sum = -1
        for p in [1, 2]:
            for tile in self.hands[p]:
                if sum(tile) > max_sum:
                    max_sum = sum(tile)
                    best_player = p
        return best_player

    def is_valid_move(self, tile):
        if not self.board: return True
        left_end = self.board[0][0]
        right_end = self.board[-1][1]
        return tile[0] == left_end or tile[1] == left_end or tile[0] == right_end or tile[1] == right_end

    def get_valid_ends(self, tile):
        if not self.board:
            return []
        ends = []
        left_end = self.board[0][0]
        right_end = self.board[-1][1]
        if tile[0] == left_end or tile[1] == left_end:
            ends.append('left')
        if tile[0] == right_end or tile[1] == right_end:
            ends.append('right')
        return ends

    def make_move(self, tile, player):
        if not self.board:
            self.board.append(tile)
        else:
            left_end = self.board[0][0]
            right_end = self.board[-1][1]
            
            if tile[1] == left_end:
                self.board.insert(0, tile)
            elif tile[0] == left_end:
                self.board.insert(0, (tile[1], tile[0]))
            elif tile[0] == right_end:
                self.board.append(tile)
            elif tile[1] == right_end:
                self.board.append((tile[1], tile[0]))
        
        self.hands[player].remove(tile)
        self.current_player = 2 if player == 1 else 1

    def make_move_with_choice(self, tile, player, side):
        left_end = self.board[0][0]
        right_end = self.board[-1][1]
        
        if side == 'left':
            if tile[1] == left_end:
                self.board.insert(0, tile)
            elif tile[0] == left_end:
                self.board.insert(0, (tile[1], tile[0]))
        else:
            if tile[0] == right_end:
                self.board.append(tile)
            elif tile[1] == right_end:
                self.board.append((tile[1], tile[0]))
        
        self.hands[player].remove(tile)
        self.current_player = 2 if player == 1 else 1

    def calculate_score(self, player):
        return sum(sum(tile) for tile in self.hands[player])


# СТИЛИЗАЦИЯ
TILE_STYLE = """
QPushButton {
    background-color: #fdfdfd;
    border: 2px solid #222;
    border-radius: 8px;
    color: #000;
    font-weight: bold;
}
QPushButton:disabled {
    background-color: #aaaaaa;
    color: #000;
}
QPushButton:hover:enabled {
    border: 2px solid #f1c40f;
    background-color: #ffffff;
    color: #000;
}
"""

BUTTON_STYLE = """
QPushButton {
    background-color: #fdfdfd;
    border: 2px solid #333;
    border-radius: 10px;
    color: #000;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
"""

RED_BUTTON_STYLE = """
QPushButton {
    background-color: #c0392b;
    border: 2px solid #333;
    border-radius: 5px;
    color: white;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #a93226;
}
"""


# ИНТЕРФЕЙС
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
        self.init_end_screen()
        self.init_overlay_screen()

    def initUI(self):
        self.setWindowTitle('Домино')
        self.setStyleSheet("QMainWindow { background-color: rgb(255,238,140); }")
        self.setGeometry(300, 300, 800, 600)
        self.setFixedSize(1540, 890)

    def init_overlay_screen(self):
        self.overlay_widget = QWidget()
        self.overlay_widget.setStyleSheet("background-color: #2c3e50;")
        layout = QVBoxLayout(self.overlay_widget)
        
        self.wait_lbl = QLabel("ПЕРЕДАЙТЕ ХОД\nСЛЕДУЮЩЕМУ ИГРОКУ")
        self.wait_lbl.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.wait_lbl.setStyleSheet("color: white;")
        self.wait_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.wait_lbl)
        layout.addStretch()
        
        self.stacked.addWidget(self.overlay_widget)

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
            btn.setFont(QFont("Arial", 22, QFont.Weight.Bold))
            btn.setStyleSheet(BUTTON_STYLE)
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
        title.setStyleSheet("color: #000; margin-top: 50px; margin-bottom: 20px; background-color: transparent;")
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
        rules_text.setStyleSheet("""
            background-color: white;
            border: 2px solid #333;
            border-radius: 15px;
            padding: 30px;
            color: #000;
        """)
        rules_text.setWordWrap(True)
        rules_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        rules_text.setFixedWidth(650)
        
        btn = QPushButton("НАЗАД")
        btn.setFixedSize(200, 60)
        btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn.setStyleSheet(BUTTON_STYLE)
        btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(rules_text, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.stacked.addWidget(widget)
            
    def init_game_screen(self):
        self.game_widget = QWidget()
        self.game_widget.setStyleSheet("background-color: rgb(255,238,140);")
        main_l = QVBoxLayout(self.game_widget)
        info_l = QHBoxLayout()

        btn_home = QPushButton("ВЕРНУТЬСЯ В МЕНЮ") 
        btn_home.setFixedSize(250, 60)
        btn_home.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_home.setStyleSheet(BUTTON_STYLE)
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

        self.board_scroll = QScrollArea()
        self.board_scroll.setWidgetResizable(True)
        self.board_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.board_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.board_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background-color: #e0b83e;
                border: none;
                height: 15px;
            }
            QScrollBar::handle:horizontal {
                background-color: #c99c2e;
                border-radius: 7px;
                min-width: 50px;
            }
        """)
        
        self.board_container = QWidget()
        self.board_container.setStyleSheet("background-color: transparent;")
        self.board_l = QGridLayout(self.board_container)
        self.board_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.board_l.setSpacing(5)
        self.board_scroll.setWidget(self.board_container)
        main_l.addWidget(self.board_scroll, 1)

        self.turn_lbl = QLabel()
        self.turn_lbl.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.turn_lbl.setStyleSheet("color: #d35400;")
        main_l.addWidget(self.turn_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.hand_area = QWidget()
        self.hand_area.setStyleSheet("background-color: transparent;")
        self.hand_l = QHBoxLayout(self.hand_area)
        self.hand_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_l.addWidget(self.hand_area)

        ctrl_l = QHBoxLayout()
        btn_baz = QPushButton("ВЗЯТЬ ИЗ БАЗАРА")
        btn_sur = QPushButton("СДАТЬСЯ")
        for b in [btn_baz, btn_sur]:
            b.setFixedSize(250, 60)
            b.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            b.setStyleSheet(RED_BUTTON_STYLE)
        
        btn_baz.clicked.connect(self.draw_bazaar)
        btn_sur.clicked.connect(self.surrender_action)
        ctrl_l.addStretch()
        ctrl_l.addWidget(btn_baz)
        ctrl_l.addWidget(btn_sur)
        ctrl_l.addStretch()
        main_l.addLayout(ctrl_l)
        self.stacked.addWidget(self.game_widget)

    def init_end_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        end_title = QLabel("КОНЕЦ ИГРЫ")
        end_title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        end_title.setStyleSheet("color: #333; margin-bottom: 40px;")
        end_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.res_lbl = QLabel()
        self.res_lbl.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.res_lbl.setStyleSheet("color: #333; margin-bottom: 30px;")
        self.res_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_lbl.setWordWrap(True)
        self.res_lbl.setMinimumWidth(600)
        
        btn = QPushButton("В МЕНЮ")
        btn.setFixedSize(350, 80)
        btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        btn.setStyleSheet(BUTTON_STYLE)
        btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        
        layout.addStretch()
        layout.addWidget(end_title)
        layout.addSpacing(30)
        layout.addWidget(self.res_lbl)
        layout.addSpacing(50)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.stacked.addWidget(widget)

    def start_new_game(self):
        self.logic.reset_game()
        self.update_ui()
        self.stacked.setCurrentIndex(2)

    def update_ui(self):
        while self.board_l.count():
            w = self.board_l.takeAt(0).widget()
            if w: w.deleteLater()

        while self.hand_l.count():
            w = self.hand_l.takeAt(0).widget()
            if w: w.deleteLater()

        for i, tile in enumerate(self.logic.board):
            if i == 0:
                btn = self.create_tile_btn(tile, enabled=False, horizontal=True)
            else:
                prev_tile = self.logic.board[i-1]
                if tile[0] == prev_tile[1]:
                    btn = self.create_tile_btn(tile, enabled=False, horizontal=True)
                else:
                    btn = self.create_tile_btn((tile[1], tile[0]), enabled=False, horizontal=True)
            self.board_l.addWidget(btn, 0, i, alignment=Qt.AlignmentFlag.AlignCenter)

        p = self.logic.current_player
        self.turn_lbl.setText(f"ХОД ИГРОКА {p}")
        for t in self.logic.hands[p]:
            btn = self.create_tile_btn(t, enabled=self.logic.is_valid_move(t))
            btn.clicked.connect(lambda ch, x=t: self.play_action(x))
            self.hand_l.addWidget(btn)

        opp = 2 if p == 1 else 1
        self.opp_lbl.setText(f"У СОПЕРНИКА: {len(self.logic.hands[opp])}")
        self.baz_lbl.setText(f"БАЗАР: {len(self.logic.bazaar)}")
        self.check_game_over()

    def create_tile_btn(self, tile, enabled=True, horizontal=False):
        is_double = (tile[0] == tile[1])
        
        if is_double:
            text = f"{tile[0]}\n—\n{tile[1]}"
            btn = QPushButton(text)
            btn.setFixedSize(55, 80)
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        else:
            if horizontal:
                text = f"{tile[0]} | {tile[1]}"
                btn = QPushButton(text)
                btn.setFixedSize(80, 55)
            else:
                text = f"{tile[0]}\n—\n{tile[1]}"
                btn = QPushButton(text)
                btn.setFixedSize(55, 80)
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        btn.setEnabled(enabled)
        btn.setStyleSheet(TILE_STYLE)
        return btn

    def check_fish(self):
        if self.logic.bazaar:
            return False
        
        can_move_any = any(self.logic.is_valid_move(t) for t in self.logic.hands[1]) or \
                       any(self.logic.is_valid_move(t) for t in self.logic.hands[2])
        
        if can_move_any:
            return False
        
        # Рыба! Определяем победителя
        s1, s2 = self.logic.calculate_score(1), self.logic.calculate_score(2)
        if s1 < s2:
            self.show_results(f"РЫБА!\nИГРОК 1: {s1} | ИГРОК 2: {s2}\nПОБЕДА ИГРОКА 1!")
        elif s2 < s1:
            self.show_results(f"РЫБА!\nИГРОК 1: {s1} | ИГРОК 2: {s2}\nПОБЕДА ИГРОКА 2!")
        else:
            self.show_results(f"РЫБА!\nИГРОК 1: {s1} | ИГРОК 2: {s2}\nНИЧЬЯ!")
        return True

    def play_action(self, tile):
        player = self.logic.current_player
        
        ends = self.logic.get_valid_ends(tile)
        
        if len(ends) == 2:
            msg = QMessageBox()
            msg.setWindowTitle("Выбор стороны")
            msg.setText(f"Костяшку {tile[0]}-{tile[1]} можно поставить с обеих сторон.\nКуда поставить?")
            msg.setIcon(QMessageBox.Icon.Question)
            btn_left = msg.addButton("Слева", QMessageBox.ButtonRole.YesRole)
            btn_right = msg.addButton("Справа", QMessageBox.ButtonRole.NoRole)
            msg.exec()
            
            if msg.clickedButton() == btn_left:
                self.logic.make_move_with_choice(tile, player, 'left')
            else:
                self.logic.make_move_with_choice(tile, player, 'right')
        else:
            self.logic.make_move(tile, player)
        
        if not self.logic.hands[player]:
            score = self.logic.calculate_score(2 if player == 1 else 1)
            self.show_results(f"ПОБЕДА ИГРОКА {player}!\nОЧКИ ПРОИГРАВШЕГО: {score}")
            return
        
        if self.check_fish():
            return
        
        self.show_transfer_screen()

    def show_transfer_screen(self):
        next_player = self.logic.current_player
        self.wait_lbl.setText(f"ХОД\nИГРОКА {next_player}")
        self.stacked.setCurrentIndex(4)
        QTimer.singleShot(3000, self.finish_transfer)

    def finish_transfer(self):
        if self.check_fish():
            return
        self.update_ui()
        self.stacked.setCurrentIndex(2)

    def draw_bazaar(self):
        current_hand = self.logic.hands[self.logic.current_player]
        can_move = any(self.logic.is_valid_move(tile) for tile in current_hand)

        if can_move:
            QMessageBox.information(self, "Внимание", "У вас есть подходящие фишки! Брать из базара не требуется.")
            return

        if self.logic.bazaar:
            self.logic.hands[self.logic.current_player].append(self.logic.bazaar.pop(0))
            self.update_ui()
        else:
            if self.check_fish():
                return
            self.logic.current_player = 2 if self.logic.current_player == 1 else 1
            self.show_transfer_screen()

    def surrender_action(self):
        winner = 2 if self.logic.current_player == 1 else 1
        self.show_results(f"ИГРОК {self.logic.current_player} СДАЛСЯ!\nПОБЕДА ИГРОКА {winner}")

    def check_game_over(self):
        if not self.logic.hands[1] and not self.logic.hands[2]:
            self.show_results("НИЧЬЯ!\nУ обоих игроков закончились фишки")
            return True
        return False

    def show_results(self, text):
        self.res_lbl.setText(text)
        self.stacked.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DominoApp()
    ex.showMaximized()
    sys.exit(app.exec())