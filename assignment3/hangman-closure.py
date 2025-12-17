# hangman-closure.py

def make_hangman(secret_word):
    """
    Returns hangman_closure(letter) function that:
      - remembers entered letters,
      - prints current word state (unguessed letters as '_'),
      - returns True if all letters are guessed, otherwise False.
    """
    guesses = []

    def hangman_closure(letter):
        # Each time it is called, the letter should be appended to guesses array
        guesses.append(letter.lower())

        # Print the word with underscores for unguessed letters
        mask = "".join(c if c in guesses else "_" for c in secret_word.lower())
        print(mask)

        # Return True if all letters have been guessed
        return all(c in guesses for c in secret_word.lower())

    return hangman_closure


if __name__ == "__main__":
    secret = input("Enter the secret word: ")
    game = make_hangman(secret)

    while True:
        guess = input("Guess a letter: ")
        if game(guess):
            print("You guessed the whole word!")
            break
