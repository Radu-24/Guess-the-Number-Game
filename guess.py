import sys
import random
import datetime
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QDialog,
    QMenuBar, QPlainTextEdit, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtGui import QFont, QIcon, QAction
from PyQt6.QtCore import Qt, QTimer
import os

class GuessTheNumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "icon.png")))
        self.history = []  # list of dicts: {'guess', 'result', 'time'}
        self.guesses = 0
        self.min_value = 1
        self.max_value = 100

        # Initial difficulty selection
        self.select_difficulty()
        self.start_new_game()

        self.init_ui()
        self.init_timer()

    def select_difficulty(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Difficulty")
        dlg_layout = QVBoxLayout(dialog)
        lbl = QLabel("Choose difficulty:")
        lbl.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dlg_layout.addWidget(lbl)

        btn_layout = QHBoxLayout()
        difficulties = [
            ("Easy (1-50)", 1, 50),
            ("Medium (1-100)", 1, 100),
            ("Hard (1-200)", 1, 200)
        ]
        for text, mn, mx in difficulties:
            btn = QPushButton(text)
            btn.setFont(QFont('Arial', 12))
            btn.clicked.connect(lambda _, a=mn, b=mx, d=dialog: self.set_difficulty(a, b, d))
            btn_layout.addWidget(btn)
        dlg_layout.addLayout(btn_layout)

        dialog.exec()

    def set_difficulty(self, mn, mx, dialog):
        self.min_value, self.max_value = mn, mx
        dialog.accept()

    def start_new_game(self):
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.guesses = 0
        self.history.clear()
        self.start_time = datetime.datetime.now()

    def init_ui(self):
        self.setWindowTitle("Guess the Number")
        self.setGeometry(100, 100, 520, 380)
        self.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")

        # Menu bar
        menubar = QMenuBar(self)
        game_menu = menubar.addMenu("Game")
        new_game_act = QAction("New Game", self)
        new_game_act.triggered.connect(self.new_game)
        history_act = QAction("Show History", self)
        history_act.triggered.connect(self.show_history)
        game_menu.addAction(new_game_act)
        game_menu.addAction(history_act)

        difficulty_menu = menubar.addMenu("Difficulty")
        change_diff_act = QAction("Change Difficulty", self)
        change_diff_act.triggered.connect(self.change_difficulty)
        difficulty_menu.addAction(change_diff_act)

        # Top layout: title + timer
        top_layout = QHBoxLayout()
        title_font = QFont('Arial', 16, QFont.Weight.Bold)
        self.label = QLabel()
        self.label.setFont(title_font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(self.label)

        self.time_label = QLabel()
        self.time_label.setFont(QFont('Arial', 12))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(self.time_label)

        # Tries label
        self.tries_label = QLabel("Tries: 0")
        self.tries_label.setFont(QFont('Arial', 12))
        self.tries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your guess...")
        self.input_box.setFont(QFont('Arial', 12))
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_box.returnPressed.connect(self.check_guess)
        self.input_box.setStyleSheet(
            "background-color: #34495e; padding: 8px; border-radius: 5px;"
        )

        # Buttons
        btn_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit Guess")
        self.submit_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.clicked.connect(self.check_guess)
        self.submit_button.setStyleSheet(
            "background-color: #e67e22; padding: 8px; border-radius: 5px;"
        )
        new_btn = QPushButton("New Game")
        new_btn.setFont(QFont('Arial', 12))
        new_btn.clicked.connect(self.new_game)
        history_btn = QPushButton("Show History")
        history_btn.setFont(QFont('Arial', 12))
        history_btn.clicked.connect(self.show_history)
        btn_layout.addWidget(self.submit_button)
        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(history_btn)

        # Result
        self.result_label = QLabel("")
        self.result_label.setFont(QFont('Arial', 12))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 30, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setMenuBar(menubar)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tries_label)
        main_layout.addWidget(self.input_box)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.result_label)
        self.setLayout(main_layout)

        # Update title now that UI exists
        self.update_title()

    def update_title(self):
        self.label.setText(f"Guess a number ({self.min_value}-{self.max_value}):")

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        elapsed = datetime.datetime.now() - self.start_time
        mins, secs = divmod(elapsed.seconds, 60)
        self.time_label.setText(f"Time: {mins:02d}:{secs:02d} | Clock: {now}")

    def check_guess(self):
        text = self.input_box.text().strip()
        if not text:
            return
        timestamp = datetime.datetime.now()
        try:
            guess_val = int(text)
        except ValueError:
            self.result_label.setText('Invalid input')
            self.result_label.setStyleSheet('color: #f1c40f;')
            self.input_box.clear()
            return

        self.guesses += 1
        elapsed = timestamp - self.start_time
        elapsed_str = f"{elapsed.seconds//60:02d}:{elapsed.seconds%60:02d}"
        # Determine result
        if guess_val < self.secret_number:
            result = 'Too low'
            color = '#e74c3c'
        elif guess_val > self.secret_number:
            result = 'Too high'
            color = '#e74c3c'
        else:
            result = 'Correct'
            color = '#2ecc71'
            self.timer.stop()  # stop stopwatch on correct
            self.input_box.setDisabled(True)
            self.submit_button.setDisabled(True)

        # Record history
        self.history.append({'guess': guess_val, 'result': result, 'time': elapsed_str})
        # Update labels
        self.tries_label.setText(f"Tries: {self.guesses}")
        self.result_label.setText(result)
        self.result_label.setStyleSheet(f'color: {color};')
        self.input_box.clear()

    def new_game(self):
        self.start_new_game()
        self.update_title()
        self.tries_label.setText("Tries: 0")
        self.result_label.setText("")
        self.input_box.setDisabled(False)
        self.input_box.clear()
        self.submit_button.setDisabled(False)
        if not self.timer.isActive():
            self.timer.start(1000)

    def change_difficulty(self):
        self.select_difficulty()
        self.new_game()

    def show_history(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Guess History")
        layout = QVBoxLayout(dlg)
        summary = QLabel(f"Total guesses: {self.guesses} | Duration: {self.history[-1]['time'] if self.history else '00:00'}")
        summary.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        layout.addWidget(summary)
        tree = QTreeWidget()
        tree.setColumnCount(3)
        tree.setHeaderLabels(["Guess", "Result", "Time"])
        groups = {}
        for entry in self.history:
            grp = entry['result']
            groups.setdefault(grp, []).append(entry)
        for grp, items in groups.items():
            parent = QTreeWidgetItem(tree, [grp])
            for e in items:
                QTreeWidgetItem(parent, [str(e['guess']), e['time'], e['result']])
        tree.expandAll()
        layout.addWidget(tree)
        dlg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuessTheNumberGame()
    window.show()
    sys.exit(app.exec())
