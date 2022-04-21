import random

number = random.randrange (1, 99)
guess = int (input ("Guess a number between 1 and 99: "))
chances = 0

while chances < 6:
	if guess == number:
		print ("You guessed the number correctly! You win!")
		break
	elif guess < number:
		print ("You need to guess higher than", guess)
		guess = int (input ("Guess a number between 1 and 99: "))
	else:
		print ("You need to guess lower than", guess)
		guess = int (input ("Guess a number between 1 and 99: "))

	chances += 1

if not chances < 6:
		print ("You lose! The number is", number)