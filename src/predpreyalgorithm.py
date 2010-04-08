#Does the work
import random
import predpreymap
import copy
import multiprocessing
from multiprocessing import Pool
from critter import Critter

best_pred = Critter("Predator")
best_prey = Critter("Prey")

def reverse(direction):
    if direction <= 3:
	direction += 3
    else:
	direction -= 3
    return direction

def left(direction):
    if direction == 1:
	return 6
    else:
        return direction - 1

def right(direction):
    if direction == 6:
	return 1
    else:
        return direction + 1

#This converts for example "Move towards predator" to "Move left"
#sensorydata holds the data from the map
#move holds a direction like "Move towards predator"
def directionConverter(sensorydata, move):
    toPred = sensorydata[1]
    toPrey = sensorydata[3]
    toPlant = sensorydata[5]

    allpossiblemoves = [toPred,  toPrey,  toPlant,
     reverse(toPred), reverse(toPrey), reverse(toPlant),
     left(toPred),    left(toPrey),    left(toPlant),
     right(toPred),   right(toPrey),   right(toPlant), 0  ]

    return allpossiblemoves[move]

def score(x):
    pred = x[0]
    prey = x[1]
    hooker = None
    if len(x) > 2:
	hooker = x[2]

    world = Map(23, 0.5)
    preds = pred.clone(4)
    preys = prey.clone(15)

    for c in preds: world.setCritterAt(world.getRandomUntakenTile(), c)
    for c in preys: world.setCritterAt(world.getRandomUntakenTile(), c)
    
    score = 0
    while len(preds) >  0 and len(preys) > 0:
	score += 1
	#For preds
	for c in preds:
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, 5)
	    location = None
	    while location == None:
                move = directionConverter(sensorydata, c.getMove(sensorydata))
		location = world.getXY(current_tile, move)
		if location == None: continue
		crit = world.getCritter(location)

		if crit == c: #If it doesn't wanna move
		    c.incrementStatus("hunger", 1)
		    break
		elif crit == None:
		    world.moveCritter(c, location)
		    c.incrementStatus("hunger", 1)
		    break
		elif crit.type == critter.PREY:
		    preys.remove(crit)
		    world.remove(crit)
		    world.moveCritter(c, location)
		    c.setStatus("hunger", 0)
		    break
		elif crit.type == critter.PREDATOR:
		    location = None

	    if c.getStatus("hunger") == 20:
		world.removeCritter(c)
		preds.remove(c)
	    hooker(world)

	for c in preys:
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, 5)
	    location = None
	    while location == None:
                move = directionConverter(sensorydata, c.getMove(sensorydata))
		location = world.getXY(current_tile, move)
		if location == None: continue
		crit = world.getCritter(location)

		if crit == c: #if the prey decides not to move
		    if world.isPlant(location):
			c.setStatus("hunger", 0)
		    else:
                        c.incrementStatus("hunger", 1)
	            break
		elif crit == None:
		    world.moveCritter(c, location)
		    if world.isPlant(location):
			c.setStatus("hunger", 0)
		    else:
                        c.incrementStatus("hunger", 1)
		    break
		elif crit.type == critter.PREY:
		    location = None
		elif crit.type == critter.PREDATOR:
		    preys.remove(c)
		    world.remove(c)
		    crit.setStatus("hunger", 0)
		    break

	    if c.getStatus("hunger") == 20:
		world.removeCritter(c)
		preys.remove(c)
	    hooker(world)

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

def mutate(gens, num_of_preds_per_gen, num_of_prey_per_gen, progress=__printProgress): 
    global best_pred, best_prey, score
    pool = Pool()

    for i in range(gens):
	progress(i, gens)

	preds = [pred for pred in best_pred.getMutations(num_of_preds_per_gen - 1)]
	preds.append(best_pred)

	preys =  [prey for prey in best_prey.getMutations(num_of_prey_per_gen - 1)]
	preys.append(best_prey)

	#Generate a Pool of processes to run all of the scoring for the predators
	predResult = pool.map_async(score, zip(preds, [copy.deepcopy(best_prey) for _ in range(num_of_preds_per_gen)]) ) 
	preyResult = pool.map_async(score, zip([copy.deepcopy(best_pred) for _ in range(len(preys))], preys) )
	
	#Parse the results
	predscores = predResult.get(None) #Probably dangerous to not specify a timeout
        #predscores = map(score, zip(preds, [copy.deepcopy(best_prey) for _ in range(num_of_preds_per_gen)]))  
	bestscore = max(predscores)
	dindex = predscores.index(bestscore)

	preyscores = preyResult.get(None)
	#preyscores = map(score, zip([copy.deepcopy(best_pred) for _ in range(len(preys))], preys) )
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
