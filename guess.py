import sys
import random
import PyQt6.QtWidgets
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class GuessTheNumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.secret_number = random.randint(1, 100)
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Guess the number between 1 and 100:")
        self.input_box = QLineEdit()
        self.submit_button = QPushButton("Submit Guess")
        self.result_label = QLabel("")

        self.submit_button.clicked.connect(self.check_guess)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Guess the Number")
        self.setGeometry(100, 100, 300, 200)

    def check_guess(self):
        try:
            guess = int(self.input.text())
            self.guesses += 1

            if guess < self.secret_number:
                self.result_label.setText('Too low!')
            elif guess > self.secret_number:
                self.result_label.setText('Too high!')
            else:
                self.result_label.setText(f'You guessed the number!')
                self.submit_button.setDisabled(True)

        except ValueError:
            self.result_label.setText('Please enter a valid number!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuessTheNumberGame()
    window.show()
    sys.exit(app.exec())
