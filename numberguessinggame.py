import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class NumberGuessingGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize game variables
        self.target = random.randint(1, 100)
        self.attempts_left = 7
        self.game_active = False

        # Set window properties
        self.setWindowTitle("Number Guessing Game")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f0f4f8;")  # Light gray-blue background

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Title label
        self.title_label = QLabel("Number Guessing Game")
        self.title_label.setFont(QFont("Helvetica", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #2c3e50;")  # Dark blue text
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Info label
        self.info_label = QLabel("Enter a number between 1 and 100.\nYou have 7 attempts.")
        self.info_label.setFont(QFont("Helvetica", 10))
        self.info_label.setStyleSheet("color: #34495e; background-color: #dfe6e9; padding: 10px; border-radius: 5px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Guess input
        self.guess_entry = QLineEdit()
        self.guess_entry.setFont(QFont("Helvetica", 12))
        self.guess_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
        """)
        self.guess_entry.setPlaceholderText("Enter your guess")
        self.guess_entry.setEnabled(False)
        self.layout.addWidget(self.guess_entry)

        # Feedback label
        self.feedback_label = QLabel("Click 'Start' to begin!")
        self.feedback_label.setFont(QFont("Helvetica", 10))
        self.feedback_label.setStyleSheet("color: #27ae60;")  # Green for feedback
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        # Attempts label
        self.attempts_label = QLabel(f"Attempts left: {self.attempts_left}")
        self.attempts_label.setFont(QFont("Helvetica", 10))
        self.attempts_label.setStyleSheet("color: #2c3e50;")
        self.attempts_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.attempts_label)

        # Start button
        self.start_button = QPushButton("Start Game")
        self.start_button.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        # Guess button
        self.guess_button = QPushButton("Submit Guess")
        self.guess_button.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.guess_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.guess_button.clicked.connect(self.check_guess)
        self.guess_button.setEnabled(False)
        self.layout.addWidget(self.guess_button)

        # Reset button
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        # Add stretch to push content up
        self.layout.addStretch()

        # Set layout
        self.setLayout(self.layout)

    def start_game(self):
        self.game_active = True
        self.target = random.randint(1, 100)
        self.attempts_left = 7
        self.guess_entry.setEnabled(True)
        self.guess_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.feedback_label.setText("Enter your guess!")
        self.attempts_label.setText(f"Attempts left: {self.attempts_left}")
        self.guess_entry.clear()
        self.info_label.setStyleSheet("color: #34495e; background-color: #dfe6e9; padding: 10px; border-radius: 5px;")

    def check_guess(self):
        if not self.game_active:
            return

        try:
            guess = int(self.guess_entry.text())
            if guess < 1 or guess > 100:
                self.feedback_label.setText("Please enter a number between 1 and 100!")
                self.feedback_label.setStyleSheet("color: #c0392b;")  # Red for error
                return

            self.attempts_left -= 1
            self.attempts_label.setText(f"Attempts left: {self.attempts_left}")

            if guess == self.target:
                self.feedback_label.setText(f"Congratulations! You guessed {self.target} correctly!")
                self.feedback_label.setStyleSheet("color: #27ae60;")  # Green for success
                self.end_game()
            elif guess < self.target:
                self.feedback_label.setText("Too low! Try a higher number.")
                self.feedback_label.setStyleSheet("color: #e67e22;")  # Orange for hint
            else:
                self.feedback_label.setText("Too high! Try a lower number.")
                self.feedback_label.setStyleSheet("color: #e67e22;")  # Orange for hint

            if self.attempts_left == 0 and guess != self.target:
                self.feedback_label.setText(f"Game Over! The number was {self.target}.")
                self.feedback_label.setStyleSheet("color: #c0392b;")  # Red for game over
                self.end_game()

        except ValueError:
            self.feedback_label.setText("Please enter a valid number!")
            self.feedback_label.setStyleSheet("color: #c0392b;")  # Red for error

        self.guess_entry.clear()

    def end_game(self):
        self.game_active = False
        self.guess_entry.setEnabled(False)
        self.guess_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.info_label.setStyleSheet("color: #34495e; background-color: #dfe6e9; padding: 10px; border-radius: 5px;")

    def reset_game(self):
        self.start_game()
        self.feedback_label.setText("Enter your guess!")
        self.feedback_label.setStyleSheet("color: #27ae60;")  # Reset to green

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NumberGuessingGame()
    game.show()
    sys.exit(app.exec_())
