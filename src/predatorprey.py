#!/usr/bin/python
#Deniz put this crap in a loop
#import predpreyalgorithm
import re	#used for regular expressions
import sys	#used for... exiting

#check validity of input
def validator(decision,max):
	result = 0
	while re.match("^[1-" + max + "]$", decision) == None:
		print("Please enter a valid choice. Try again.\n")
		decision = raw_input("Your decision?\n")
	result = decision
	return result

while True:
	print("\nChoose an option below, type the corresponding number, then hit the return key.")
	print("1.Run simulation")
	print("2.Help!")
	print("3.Exit")
	main_choice = raw_input("Your decision?\n")
	main_choice = validator(main_choice,"3")

	main_choice = int(main_choice)
	while main_choice == 1:
		print("\nStarting Simulation!")
		print("1.Save")
		print("2.Load")
		print("3.Set Behavior")
		print("4.Animate")
		print("5.Help")
		print("6.Main Menu")
		sub_choice_1 = raw_input("Your decision?\n")
		sub_choice_1 = validator(sub_choice_1,"6")

		sub_choice_1 = int(sub_choice_1)
		if sub_choice_1 == 1:
			print("SAVE Stuff")
		if sub_choice_1 == 2:
			print("Load Stuff")
		if sub_choice_1 == 3:
			print("Edit behaviors!")
		if sub_choice_1 == 4:
			print("Animate Stuff!")
		if sub_choice_1 == 5:
			print("Help File")
		if sub_choice_1 == 6:
			print("Returning to Main Menu...")
			break;
		
		#generations = input("How many generations would you like this to run for?")
		#num_of_preds_per_gen = input("How many predators would you like per generation?")
		#num_of_prey_per_gen = input("How many prey would you like per generation?")
		#wanna_set_behavior = input("Would you like to set predator behavior? (yes,no)")
	if main_choice == 2:
		print("Help File")
	if main_choice == 3:
		sys.exit("Come back soon.\n")

#	save_pred = input("Input the filename of the predator you'd like to save.")
#	save_prey = input("Input the filename of the prey you'd like to save.")
#
#	load_pred = input("Input the filename of the predator you'd like to load.")
#	load_prey = input("Input the filename of the prey you'd like to loada.")



	#predpreyalgorithm.mutate(generations, num_of_preds_per_gen, num_of_prey_per_gen)
	#print(predpreyalgorithm.best_pred[0])
	#print(predpreyalgorithm.best_prey[0])
