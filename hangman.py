import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.words = [
            ("python", "A popular programming language"),
            ("computer", "An electronic device for processing data"),
            ("keyboard", "Input device with keys"),
            ("sunshine", "Bright light from the sun"),
            ("bicycle", "A two-wheeled vehicle"),
            ("library", "A place with lots of books"),
            ("pizza", "A savory dish with toppings"),
        ]
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Hangman Game with Hints")
        self.setFixedSize(500, 600)
        self.setStyleSheet("background-color: #f0f4f8;")  # Light gray-blue background

        # Create main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Title label
        self.title_label = QLabel("Hangman Game")
        self.title_label.setFont(QFont("Helvetica", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #2c3e50;")  # Dark blue text
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Hint label
        self.hint_label = QLabel("Hint: Select a word to start")
        self.hint_label.setFont(QFont("Helvetica", 10))
        self.hint_label.setStyleSheet("color: #34495e; background-color: #dfe6e9; padding: 10px; border-radius: 5px;")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.hint_label)

        # Word display
        self.word_label = QLabel("_ _ _ _ _ _")
        self.word_label.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.word_label.setStyleSheet("color: #2c3e50; background-color: #ffffff; padding: 10px; border-radius: 5px;")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.word_label)

        # Attempts label
        self.attempts_label = QLabel("Attempts left: 6")
        self.attempts_label.setFont(QFont("Helvetica", 10))
        self.attempts_label.setStyleSheet("color: #2c3e50;")
        self.attempts_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.attempts_label)

        # Feedback label
        self.feedback_label = QLabel("Enter a letter to start!")
        self.feedback_label.setFont(QFont("Helvetica", 10))
        self.feedback_label.setStyleSheet("color: #27ae60;")  # Green for initial message
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        # Input layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)

        # Guess input
        self.guess_entry = QLineEdit()
        self.guess_entry.setFont(QFont("Helvetica", 12))
        self.guess_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #ffffff;
                max-width: 50px;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
            QLineEdit:disabled {
                border-color: #95a5a6;
                background-color: #ecf0f1;
            }
        """)
        self.guess_entry.setPlaceholderText("Letter")
        self.guess_entry.setMaxLength(1)
        self.input_layout.addWidget(self.guess_entry)

        # Guess button
        self.guess_button = QPushButton("Guess")
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
        self.input_layout.addWidget(self.guess_button)

        self.layout.addLayout(self.input_layout)

        # Used letters label
        self.used_letters_label = QLabel("Used letters: None")
        self.used_letters_label.setFont(QFont("Helvetica", 10))
        self.used_letters_label.setStyleSheet("color: #34495e;")
        self.used_letters_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.used_letters_label)

        # Play again button
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.play_again_button.setStyleSheet("""
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
        self.play_again_button.clicked.connect(self.reset_game)
        self.play_again_button.setEnabled(False)
        self.layout.addWidget(self.play_again_button)

        # Add stretch to push content up
        self.layout.addStretch()

        # Set layout
        self.setLayout(self.layout)

        # Initialize game state
        self.max_attempts = 6  # Set maximum attempts to 6
        self.reset_game()

    def reset_game(self):
        # Initialize or reset game state
        self.word, self.hint = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = self.max_attempts
        self.game_active = True
        self.guess_entry.setEnabled(True)
        self.guess_button.setEnabled(True)
        self.play_again_button.setEnabled(False)
        self.feedback_label.setText("Enter a letter to start!")
        self.feedback_label.setStyleSheet("color: #27ae60;")
        self.hint_label.setText(f"Hint: {self.hint}")
        self.word_label.setText(self.display_word())
        self.attempts_label.setText(f"Attempts left: {self.attempts_left}")
        self.used_letters_label.setText("Used letters: None")
        self.guess_entry.clear()

    def display_word(self):
        # Display the word with underscores for unguessed letters
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)

    def check_guess(self):
        if not self.game_active:
            return

        guess = self.guess_entry.text().strip().lower()
        self.guess_entry.clear()

        if not guess or len(guess) != 1 or not guess.isalpha():
            self.feedback_label.setText("Please enter a single letter!")
            self.feedback_label.setStyleSheet("color: #c0392b;")  # Red for error
            return

        if guess in self.guessed_letters:
            self.feedback_label.setText("You've already guessed that letter!")
            self.feedback_label.setStyleSheet("color: #e67e22;")  # Orange for warning
            return

        self.guessed_letters.add(guess)
        self.update_used_letters()

        if guess in self.word:
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet("color: #27ae60;")  # Green for success
            self.word_label.setText(self.display_word())
            if all(letter in self.guessed_letters for letter in self.word):
                self.feedback_label.setText(f"You won! The word was '{self.word}'!")
                self.end_game()
        else:
            self.attempts_left -= 1
            self.attempts_label.setText(f"Attempts left: {self.attempts_left}")
            self.feedback_label.setText("Incorrect!")
            self.feedback_label.setStyleSheet("color: #c0392b;")  # Red for incorrect
            if self.attempts_left == 0:
                self.feedback_label.setText(f"Game Over! The word was '{self.word}'.")
                self.end_game()

    def update_used_letters(self):
        # Update the display of used letters
        used = sorted(self.guessed_letters) if self.guessed_letters else ["None"]
        self.used_letters_label.setText(f"Used letters: {', '.join(used)}")

    def end_game(self):
        # End the game and disable input
        self.game_active = False
        self.guess_entry.setEnabled(False)
        self.guess_button.setEnabled(False)
        self.play_again_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
