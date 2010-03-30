import Map
import random

def hunger(map, critter):
    return (5, Map.topleft)

def fear(map, critter):
    return (3, Map.topleft)

#Yes I can just put functions into an array like this in python
preyfunctions = [hunger, fear]
predfunctions = [hunger]

def getPredatorNextMove(map, predator):
	#Stupid implementation that ignores votes, just picks a random function
	#passes it the arguements and returns the move that the function chose
	global predfunctions
	return random.choice(predfunctions)(map, predator)[1]

def getPreyNextMove(map, prey):
	#Stupid implementation that ignores votes, just picks a random function
	#passes it the arguements and returns the move that the function chose
	global preyfunctions
	return random.choice(preyfunctions)(map, prey)[1]
