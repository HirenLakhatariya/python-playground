import random
from logic import NumberGuessingGame

class game:
    def __init__(self):
        var = input("Welcome to the number guessing game! Press enter to play ")
        self.play()


    def play(self):
            while True:
                random_number = random.randint(1, 100)
                logic = NumberGuessingGame(random_number)
                while True:
                    guess = input("Guess a number between 1 and 100 : ")
                    if not guess.isdigit():
                        print("Please enter valid Number ")
                        continue
                    result = logic.check_guess(int(guess))
                    if result == "correct":
                        print("🎉 Congratulations! You won!")
                        break
                    elif result == "high":
                        print("Too high!")
                    elif result == "low":
                        print("Too low!")
                again = input("Do you want to play again? (y/n)").lower()
                if again != "y":
                    break

game()