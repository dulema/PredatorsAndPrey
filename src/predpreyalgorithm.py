#Does the work
import random
from predpreymap import Map
import copy
#import multiprocessing
#from multiprocessing import Pool
from critter import Critter
import critter

best_pred = Critter(critter.PREDATOR)
best_prey = Critter(critter.PREY)

def reverse(direction):
    if direction == None or direction == 0:
	return 0
    if direction <= 3:
	direction += 3
    else:
	direction -= 3
    return direction

def left(direction):
    if direction == None or direction == 0:
	return 0
    if direction == 1:
	return 6
    else:
        return direction - 1

def right(direction):
    if direction == None or direction == 0:
	return 0
    if direction == 6:
	return 1
    else:
        return direction + 1

#This converts for example "Move towards predator" to "Move left"
#sensorydata holds the data from the map
#move holds a direction like "Move towards predator"
def directionConverter(sensorydata, move):
    if sensorydata == (None, None, None, None, 0, 0):
	return random.randint(0, 6)
    toPred = sensorydata[1]
    toPrey = sensorydata[3]
    toPlant = sensorydata[5]

    toPred = 0 if toPred == None else toPred
    toPrey = 0 if toPrey == None else toPrey
    toPlant = 0 if toPlant == None else toPlant
    allpossiblemoves = [toPred,  toPrey,  toPlant,
     reverse(toPred), reverse(toPrey), reverse(toPlant),
     left(toPred),    left(toPrey),    left(toPlant),
     right(toPred),   right(toPrey),   right(toPlant), 0  ]
    #print( "%s -> %s" % (move, allpossiblemoves[move]) )
    return allpossiblemoves[move]

def score(x):
    pred = x[0]
    prey = x[1]
    hooker = None
    if len(x) > 2:
	hooker = x[2]

    world = Map(23, 0.5)
    for p in pred.clone(4): world.setCritterAt(world.getRandomUntakenTile(), p)
    for p in prey.clone(14): world.setCritterAt(world.getRandomUntakenTile(), p)
    
    score = 0
    while len(world.getPreys()) >  0 and len(world.getPredators()) > 0:
	print(len(world.getPreys()), len(world.getPredators()))
        #Score get incremented because it is just how every long the species lasts
	score += 1

	#Increment the hunger of all of the animals by 1
        for c in world.getCritters():
		c.incrementStatus("hunger", 1)
                if c.getStatus("hunger") >= 20:
			world.removeCritter(c)

	for c in world.getPredators():
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, 20)
	    print(sensorydata)
	    location = None
	    move = None
	    while True:
		print("pred looping")
		while location in (None, (-1, -1)):
		    print("pred location loop")
                    critmove = c.getMove(sensorydata) 
		    print(sensorydata, critmove)
		    move = directionConverter(sensorydata,critmove ) 
		    location = world.getCritterDest(c,move)
		crit = world.getCritterAt(location)

		if crit == c: #If it doesn't wanna move
		    print("crit == c")
		    break
		elif crit == None:
		    world.moveCritter(c, move)
		    print("crit == None")
		    break
		elif crit.type == critter.PREY:
		    world.removeCritter(crit)
		    world.moveCritter(c, move)
		    c.setStatus("hunger", 0)
		    print("crit.type == critter.PREY")
		    break
		elif crit.type == critter.PREDATOR:
		    location = None
		else:
		    print("pred WTFFF?")

	    if hooker != None:
		    hooker(world, score)

	for c in world.getPreys():
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, 20)
	    location = None
	    while True:
		print("prey looping")
		while location in (None, (-1, -1) ): 
		    print("prey location loop")
		    critmove = c.getMove(sensorydata)
		    print(sensorydata, critmove)
		    move = directionConverter(sensorydata,critmove )
		    location = world.getCritterDest(c, move)
		crit = world.getCritterAt(location)

		if crit == c: #if the prey decides not to move
		    if world.isPlant(location):
			c.setStatus("hunger", 0)
		    print("crit == c")
	            break
		elif crit == None:
		    world.moveCritter(c, move)
		    if world.isPlant(location):
			c.setStatus("hunger", 0)
		    print("crit == None")
		    break
		elif crit.type == critter.PREY:
		    location = None
		    print("self")
		elif crit.type == critter.PREDATOR:
		    world.removeCritter(c)
		    crit.setStatus("hunger", 0)
		    print("crit.type == critter.PREDATOR")
		    break
		else:
		    print("WTF?")

            if hooker != None:
		    hooker(world, score)

    return score

def __printProgress(num, total):
    width = 40
    s = "%d/%d [" % (num, total)
    completecount = (float(num)/total)*40
    for i in range(40):
	if i < completecount:
	    s = s + "="
	else:
	    s = s + "-"
    s = s + "]\r"
    print s,
    import sys
    sys.stdout.flush()

def __clearProgress():
    print "                                                                         \n",
    import sys
    sys.stdout.flush()


def roundprogress(map, score):
	pass
    	#print("Progress at %s" % score)
    #	for critter in map.critters: print("%s at %s hunger:%s" % (critter.type, map.critters[critter], critter.getStatus("hunger")))

def mutate(gens, num_of_preds_per_gen, num_of_prey_per_gen, progress=__printProgress): 
    global best_pred, best_prey, score
    #pool = Pool()

    for i in range(gens):
	progress(i, gens)

	preds = [pred for pred in best_pred.getMutations(num_of_preds_per_gen - 1)]
	preds.append(best_pred)

	preys =  [prey for prey in best_prey.getMutations(num_of_prey_per_gen - 1)]
	preys.append(best_prey)

	#Generate a Pool of processes to run all of the scoring for the predators
	#predResult = pool.map_async(score, zip(preds, [copy.deepcopy(best_prey) for _ in range(num_of_preds_per_gen)]) ) 
	#preyResult = pool.map_async(score, zip([copy.deepcopy(best_pred) for _ in range(len(preys))], preys) )
	
	#Parse the results
	#predscores = predResult.get(None) #Probably dangerous to not specify a timeout
	predscores = []
	for p in preds:
		predscores.append(score((p, copy.deepcopy(best_prey), roundprogress)))
        #predscores = map(score, zip(preds, [copy.deepcopy(best_prey) for _ in range(len(preds))], [roundprogress for _ in range(len(preds))] )   )
	bestscore = max(predscores)
	dindex = predscores.index(bestscore)

	#preyscores = preyResult.get(None)
	#preyscores = map(score, zip([copy.deepcopy(best_pred) for _ in range(len(preys))], preys) )
	preyscores = []
	for p in preys:
		preyscores.append(score((copy.deepcopy(best_pred), p, roundprogress)))
	bestscore = max(preyscores)
	yindex = preyscores.index(bestscore)

	best_prey = preys[yindex]
	best_pred = preds[dindex]
	
if __name__ == "__main__":
    gens = input("How many generations?")	
    preds = input("How many preds per generations?")	
    preys = input("How many preys per generations?")	
    mutate(gens, preds, preys)
    __clearProgress()
    print(best_pred.type)
    print(best_prey.type)
