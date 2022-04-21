import time
import random


def DisplayIntro():
    print("This is the story of Dali.")
    time.sleep(5)
    print("He is a cat of the highest standard, you could call him the greatest being in the universe and he would not mind at all.")
    time.sleep(8)
    print("Few people, if any at all, has ever grasped the beauty and elegance of his chest, it requires alot of maintance to keep its grandiose bulge.")
    time.sleep(11)
    print("More food is always needed but never given from the Master.")
    time.sleep(6)
    print("The Master is his owner by the name Anouk.")
    time.sleep(6)
    print("The caretaker, the giver, the one who provides, she goes by many names.")
    time.sleep(6)
    print()
    print("---------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    time.sleep(4)
    print("Today you will help Dali aquire nutrients to keep the chest at the godly level it deserves!")
    time.sleep(6)
    print("It is morning and the one who provides has not gone up to give food yet.")
    time.sleep(6)
    print()
    print("Should you:")
    time.sleep(5)
    print("1: Use the awesomeness of the chest to stop the airflow from the caretakers mouth to get the wanted attention.")
    time.sleep(6)
    print()
    print("Or")
    print()
    time.sleep(5)
    print("2: Go to the cupboard and try to get it yourself.")


def ChoosePath():
	Path = ""
	while Path != "1" and Path != "2": # input validation
		Path = input("Which path will you choose? (1 or 2): ")

	return Path


def CheckPath(ChosenPath):
	print("You choose to put the chest before everything else yet again, as you should.")

	CorrectPath = random.radint(1, 2)

	if ChosenPath == str(CorrectPath):
		print("The way you handled it was rewarded with that sweet life juice, called food.")
	else:
		print("A big surge of hunger flows through you. Life is miserable.")


PlayAgain = "yes"
while PlayAgain == "yes" or PlayAgain == "y":
	DisplayIntro()
    Choice = ChoosePath()
    CheckPath(Choice) # Choice is equal to "1" or "2"
    PlayAgain = input("Do you want to play again? (yes or y to continue playing): ")