import random

class RockPaperScissor:
    def __init__(self):
        self.choices = ["rock", "paper", "scissor"]
        self.play()

    def play(self):
        print("Welcome to Rock Paper Scissor!")
        input("Press Enter to continue...")

        while True:
            user_choice = input("Enter your choice (rock/paper/scissor or exit): ").lower()

            if user_choice == "exit":
                print("Thanks for playing!")
                break

            if user_choice not in self.choices:
                print("Invalid choice")
                continue

            computer_choice = random.choice(self.choices)
            print(f"Computer chose: {computer_choice}")

            if user_choice == computer_choice:
                print("It's a tie!\n")
            elif (
                (user_choice == "rock" and computer_choice == "scissor") or
                (user_choice == "scissor" and computer_choice == "paper") or
                (user_choice == "paper" and computer_choice == "rock")
            ):
                print("You win!\n")
            else:
                print("Computer wins!\n")

RockPaperScissor()