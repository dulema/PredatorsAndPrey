#!/usr/bin/python
import predpreyalgorithm
import re			#used for regular expressions
import sys			#used for exiting

#check validity of input
def validator(decision,min,max):
	result = 0
	while re.match("^[" + min + "-" + max + "]$", decision) == None:
		print("Please enter a valid choice. Try again.\n")
		decision = raw_input("Your decision?\n")
	result = decision
	return result

#view the help file
def helpfile():
	f = open("help.txt", "r")
	print("")
	for line in f:
        	print line,
	print("")

#1 = pred, 2 = prey
def savecritter(type, name):
	#critter.save(f)
	if type == 1:
		print("SAVING " + name + ".predator")
		try:
			f = open("critters/" + name + ".predator",'w')
			f.write("Hungry! VERY HUNGRY!\n")
		except IOError:
			print("Error saving " + name + ".predator!\n")
	if type == 2:
		print("SAVING " + name + ".prey")
		try:
			f = open("critters/" + name + ".prey",'w')
			f.write("SCARED OF THE WORLD!\n")
		except IOError:
			print("Error saving " + name + ".prey!\n")

def loadcritter(type, name):
	#critter.load(f)
	if type == 1:
		print("LOADING " + name + ".predator")
		try:
			f = open("critters/" + name + ".predator",'r')
			print("here comes the predator info...")
			for line in f:
	        		print line,
				print(eval(line))#needs work
		except IOError:
			print("Error opening " + name + ".predator!\n")

	if type == 2:
		print("LOADING" + name + ".prey")
		try:
			f = open("critters/" + name + ".prey",'r')
			print("here comes the prey info...")
			for line in f:
	        		print line,
				print(eval(line))#needs work
		except IOError:
			print("Error opening " + name + ".prey!\n")

simulation_run_through = 0
generations = 0
world_size = 0

while True:
	print("Choose an option below, type the corresponding number, then hit the return key.")
	print("1.Run simulation")
	print("2.Help!")
	print("3.Exit")
	main_choice = raw_input("Your decision?\n")
	main_choice = validator(main_choice,"1","3")
	main_choice = int(main_choice)

	while main_choice == 1:
		if simulation_run_through == 0:
			print("Please set the initial parameters as follows...")
			generations = raw_input("How many generations would you like this to run for?\n")
			while re.match("^[0-9]+$",generations) == None:
				print("Please input a valid number of generations.")
				generations = raw_input("How many generations would you like this to run for?\n")
			generations = int(generations)

			world_size = raw_input("Enter the size of the world.\n")#square,so input of 10=10*10=100 tiles
			while re.match("^[0-9]+$",world_size) == None:
				print("Please input a valid world size.")
				world_size = raw_input("Enter the size of the world.\n")
			world_size = int(world_size)
			tile_num = (world_size * world_size)
			print("There will be " + str(tile_num) + " tiles in the world.")
			print("\nStarting Simulation!")

		#predpreyalgorithm.mutate(generations, 5, 5)
		#print(predpreyalgorithm.best_pred)
		#print(predpreyalgorithm.best_prey)
		
		print("1.Save")
		print("2.Load")
		print("3.View animation")
		print("4.Start simulation again?")
		print("5.Help")
		print("6.Main Menu")
		sub_choice_1 = raw_input("Your decision?\n")
		sub_choice_1 = validator(sub_choice_1,"1","6")
		sub_choice_1 = int(sub_choice_1)
		
		if sub_choice_1 == 1:
			print("You can save either...")
			print("1.Predator")
			print("2.Prey")
			save_choice = raw_input("Which type of critter would you like to save?\n")
			save_choice = validator(save_choice,"1","2")
			save_choice = int(save_choice)
			if save_choice == 1:
				save_name = raw_input("Please name the predator.\n")
			if save_choice == 2:
				save_name = raw_input("Please name the prey.\n")
			savecritter(save_choice, save_name)
		if sub_choice_1 == 2:
			print("You can load either...")
			print("1.Predator")
			print("2.Prey")
			load_choice = raw_input("Which type of critter would you like to load?\n")
			load_choice = validator(load_choice,"1","2")
			load_choice = int(load_choice)
			if load_choice == 1:
				load_name = raw_input("Please enter the name of the predator.\n")
			if load_choice == 2:
				load_name = raw_input("Please enter the name of the prey.\n")
			loadcritter(load_choice, load_name)
		if sub_choice_1 == 3:
			print("Animate Stuffs!!")
		if sub_choice_1 == 4:
			simulation_run_through = -1
		if sub_choice_1 == 5:
			helpfile()
		if sub_choice_1 == 6:
			print("Returning to Main Menu...")
			break

		simulation_run_through+=1

	if main_choice == 2:
		helpfile()
	if main_choice == 3:
		sys.exit("Come back soon!\n")

