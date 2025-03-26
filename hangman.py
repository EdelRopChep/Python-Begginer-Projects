import random


def hangman():
    # Word categories
    categories = {
        "Animals": ["elephant", "giraffe", "kangaroo", "rhinoceros", "crocodile"],
        "Countries": ["canada", "brazil", "japan", "australia", "germany"],
        "Fruits": ["pineapple", "watermelon", "strawberry", "blueberry", "raspberry"]
    }

    # Hangman ASCII art stages
    hangman_stages = [
        """
          +---+
          |   |
              |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         /    |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         / \\  |
              |
        =========
        """
    ]

    # Game setup
    wins = 0
    losses = 0

    print("Welcome to Hangman!")

    while True:
        # Select category
        print("\nChoose a category:")
        for i, category in enumerate(categories.keys(), 1):
            print(f"{i}. {category}")

        try:
            choice = int(input("Enter category number: ")) - 1
            if choice < 0 or choice >= len(categories):
                print("Invalid choice. Please try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        category_name = list(categories.keys())[choice]
        secret_word = random.choice(categories[category_name]).lower()
        guessed_letters = []
        attempts_left = 6
        word_progress = ["_"] * len(secret_word)

        print(f"\nCategory: {category_name}")
        print(f"Word has {len(secret_word)} letters.")
        print(" ".join(word_progress))

        while attempts_left > 0 and "_" in word_progress:
            # Get player's guess
            guess = input("\nGuess a letter: ").lower()

            # Validate input
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter!")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter!")
                continue

            guessed_letters.append(guess)

            # Check if letter is in the word
            if guess in secret_word:
                print("Correct!")
                # Update word progress
                for i in range(len(secret_word)):
                    if secret_word[i] == guess:
                        word_progress[i] = guess
            else:
                attempts_left -= 1
                print(f"Wrong! Attempts left: {attempts_left}")
                print(hangman_stages[6 - attempts_left])

            # Display current status
            print(" ".join(word_progress))
            print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")

        # Game result
        if "_" not in word_progress:
            print(f"\nCongratulations! You guessed the word: {secret_word}")
            wins += 1
        else:
            print(f"\nGame over! The word was: {secret_word}")
            losses += 1
            print(hangman_stages[-1])  # Show full hangman

        # Display stats
        print(f"\nWins: {wins} | Losses: {losses}")

        # Play again?
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break


# Start the game
hangman()
