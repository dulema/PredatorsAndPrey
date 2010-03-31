#!/usr/bin/python
#Deniz put this crap in a loop
#import predpreyalgorithm
import re	#used for regular expressions
import sys	#used for... exiting

while True:
	print("Choose an option below, type the corresponding number, then hit the return key.")
	print("1.Run simulation")
	print("2.Animate!")
	print("3.Load a critter")
	print("4.Help!")
	print("5.Exit")
	main_choice = raw_input("Your decision?")
	while re.match("^[1-5]$", main_choice) == None:
		print("Please enter a valid choice. Try again.")
		main_choice = raw_input("Your decision?")
	main_choice = int(main_choice)
	if main_choice == 1:
		print("Starting Simulation! Set initial parameters.")
		#generations = input("How many generations would you like this to run for?")
		#num_of_preds_per_gen = input("How many predators would you like per generation?")
		#num_of_prey_per_gen = input("How many prey would you like per generation?")
		#wanna_set_behavior = input("Would you like to set predator behavior? (yes,no)")
		#if wanna_set_behavior == yes:
	if main_choice == 2:
		print("Choice 2")
	if main_choice == 3:
		print("Choice 3")
	if main_choice == 4:
		print("Choice 4")
	if main_choice == 5:
		sys.exit("Come back soon.");

#	save_pred = input("Input the filename of the predator you'd like to save.")
#	save_prey = input("Input the filename of the prey you'd like to save.")
#
#	load_pred = input("Input the filename of the predator you'd like to load.")
#	load_prey = input("Input the filename of the prey you'd like to loada.")



	#predpreyalgorithm.mutate(generations, num_of_preds_per_gen, num_of_prey_per_gen)
	#print(predpreyalgorithm.best_pred[0])
	#print(predpreyalgorithm.best_prey[0])
