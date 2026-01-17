class NumberGuessingGame:
    def __init__(self,number):
        self.number = number
    
    def check_guess(self,guess):
        if guess == self.number:
            return "correct"
        elif guess < self.number:
            return "low"
        else:
            return "high"