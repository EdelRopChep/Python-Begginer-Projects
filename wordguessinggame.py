import random


def word_guessing_game():
    # List of possible words
    word_list = ["eldoret", "nairobi", "kitale", "mombasa", "kisumu", "nakuru", "kiambu"]

    # Select a random word from the list
    secret_word = random.choice(word_list).lower()
    guessed_letters = []
    attempts = 6  # Number of allowed incorrect guesses
    word_progress = ["_"] * len(secret_word)

    print("Welcome to the Word Guessing Game!")
    print("Guess the word one letter at a time.")
    print(" ".join(word_progress))

    while attempts > 0 and "_" in word_progress:
        try:
            # Get player's guess
            guess = input("Enter a letter: ").lower()

            # Validate input
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter!")
                continue

            # Check if letter was already guessed
            if guess in guessed_letters:
                print("You already guessed that letter!")
                continue

            guessed_letters.append(guess)

            # Check if letter is in the word
            if guess in secret_word:
                print("Correct!")
                # Update word progress with correctly guessed letters
                for i in range(len(secret_word)):
                    if secret_word[i] == guess:
                        word_progress[i] = guess
            else:
                attempts -= 1
                print(f"Wrong! You have {attempts} attempts remaining.")

            # Display current progress
            print(" ".join(word_progress))
            print(f"Guessed letters: {', '.join(guessed_letters)}")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Game over message
    if "_" not in word_progress:
        print(f"Congratulations! You guessed the word: {secret_word}")
    else:
        print(f"Game over! The word was: {secret_word}")


# Start the game
word_guessing_game()
