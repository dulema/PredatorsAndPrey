#!/usr/bin/python
#Deniz put this crap in a loop
import PredPreyAlgorithm

generations = input("How many generations would you like this to run for?")
num_of_preds_per_gen = input("How many predators would you like per generation?")
num_of_prey_per_gen =  input("How many prey would you like per generation?")

PredPreyAlgorithm.mutate(generations, num_of_preds_per_gen, num_of_prey_per_gen)
print(PredPreyAlgorithm.best_pred)
print(PredPreyAlgorithm.best_prey)
