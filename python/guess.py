# This is just one possible solution of many.
# It could be simpler or more complex as needed.

import random
import math

low = 1
high = 1000

maxGuesses = int(round(math.log(high - low, 2)))
currentGuesses = 0

stillPlaying = True

hiddenNumber = random.randrange(low, high)

print "You have " + str(maxGuesses - currentGuesses) + \
      " chances to guess the hidden number. Please guess a number between " + \
      str(low) + " and " + str(high) + ":"

while currentGuesses < maxGuesses and stillPlaying:
	myNumber = int(raw_input())

	currentGuesses += 1

	if myNumber == hiddenNumber:
		print "You win!"
		stillPlaying = False

	elif myNumber < hiddenNumber:
		print "Too low. You have " + str(maxGuesses - currentGuesses) + " guesses left."

	elif myNumber > hiddenNumber:
		print "Too high. You have " + str(maxGuesses - currentGuesses) + " guesses left."
	
	if currentGuesses >= maxGuesses:
		stillPlaying = False	

	if stillPlaying:
		print "Try again:"

print "The hidden number was " + str(hiddenNumber) + "."
