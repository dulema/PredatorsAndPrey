#!/usr/bin/python
#Deniz put this crap in a loop
import predpreyalgorithm

generations = input("How many generations would you like this to run for?")
num_of_preds_per_gen = input("How many predators would you like per generation?")
num_of_prey_per_gen =  input("How many prey would you like per generation?")

predpreyalgorithm.mutate(generations, num_of_preds_per_gen, num_of_prey_per_gen)
print(predpreyalgorithm.best_pred[0])
print(predpreyalgorithm.best_prey[0])
