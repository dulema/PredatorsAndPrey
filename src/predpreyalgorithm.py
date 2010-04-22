#Does the work
import random
from predpreymap import Map
import copy
from critter import Critter
import critter

best_pred = Critter(critter.PREDATOR)
best_prey = Critter(critter.PREY)
DEFAULT_SETTINGS = {"mapsize":20, "vegpercent":0.5, "preypercent":0.1, "predpercent":0.1, "sight":10}


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
    #print(sensorydata)
    if sensorydata == (None, None, None, None, 0, 0) or (None, None, None, None, None, None):
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
    return allpossiblemoves[move]

def calcscore(x):
    pred = x[0]
    prey = x[1]

    settings = x[2] if len(x) > 2 else DEFAULT_SETTINGS
    mapsize = settings["mapsize"] if "mapsize" in settings else 20
    vegpercent = settings["vegpercent"] if "vegpercent" in settings else 0.5
    #plantbites = 3
    plantbites = ufaufaufa
    preypercent = settings["preypercent"] if "preypercent" in settings else 0.1
    predpercent = settings["predpercent"] if "predpercent" in settings else 0.1
    maxhunger = settings["maxhunger"] if "maxhunger" in settings else 20
    sight = settings["sight"] if "sight" in settings else 20

    #print("mapsize=%d, vegpercent=%.2f, preypercent=%.2f, predpercent=%.2f, maxhunger=%d, sight=%d" % (mapsize, vegpercent, preypercent, predpercent, maxhunger, sight))

    hooker = x[3] if len(x) > 3 else None

    world = Map(mapsize, vegpercent,plantbites)
    for p in pred.clone(int((mapsize**2)*predpercent)): world.setCritterAt(world.getRandomUntakenTile(), p)
    for p in prey.clone(int((mapsize**2)*preypercent)): world.setCritterAt(world.getRandomUntakenTile(), p)

    score = 0
    while len(world.getPreys()) >  0 and len(world.getPredators()) > 0:
        #Score get incremented because it is just how every long the species lasts
	score += 1

	#Increment the hunger of all of the animals by 1
        for c in world.getCritters():
		c.incrementStatus("hunger", 1)
                if c.getStatus("hunger") >= maxhunger:
			world.removeCritter(c)

	for c in world.getPredators():
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, sight)
	    location = None
	    move = None
	    loopcount = 0
	    while loopcount <= 40:
		loopcount += 1
		while location in (None, (-1, -1)):
		    #print("pred loc loop")
                    critmove = c.getMove(sensorydata) 
		    move = directionConverter(sensorydata,critmove ) 
		    #print "Pred move:",move 
		    location = world.getCritterDest(c,move)
		crit = world.getCritterAt(location)

		if crit == c: #If it doesn't wanna move
		    print("pred: Hello me!!")
		    break
		elif crit == None:
		    world.moveCritter(c, move)
		    break
		elif crit.type == critter.PREY:
		    world.removeCritter(crit)
		    world.moveCritter(c, move)
		    c.setStatus("hunger", 0)
		    break
		elif crit.type == critter.PREDATOR:
		    location = None
		else:
		    raise Exception("Unhandled case for preds")

	    if hooker != None:
		    hooker(world, score)

	for c in world.getPreys():
	    current_tile = world.getCritterXY(c)
	    sensorydata = world.getSensoryData(c, sight)
	    location = None
	    loopcount = 0
	    while loopcount <= 40:
		loopcount += 1
		while location in (None, (-1, -1) ): 
		    #print("prey loc loop")
		    critmove = c.getMove(sensorydata)
		    move = directionConverter(sensorydata, critmove)
		    #print "Prey move:",move 
		    location = world.getCritterDest(c, move)
		crit = world.getCritterAt(location)

		if crit == c: #if the prey decides not to move
		    print("prey: Hello me!!")
		    #Returns Two Parm, One Of Boolean Other Is Health
		    if (world.isPlant(location)):
			c.setStatus("hunger", 0)
	            break
		elif crit == None:
		    world.moveCritter(c, move)
		    #Returns Two Parm, One Of Boolean Other Is Health
		    if (world.isPlant(location):
			c.setStatus("hunger", 0)
		    break
		elif crit.type == critter.PREY:
		    location = None
		elif crit.type == critter.PREDATOR:
		    world.removeCritter(c)
		    crit.setStatus("hunger", 0)
		    break
		else:
		    raise Exception("Unhandled case for preys")

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


def getCalcScoreArgs(preds, preys, bpred, bprey, settings):
    bpreyclones = [copy.deepcopy(bprey) for _ in preds]
    bpredclones = [copy.deepcopy(bpred) for _ in preys]
    settingsclones = [settings for _ in range(max(len(preds),len(preys)))]
    predArgs = zip(preds, bpreyclones, settingsclones[:len(preds)])
    preyArgs = zip(bpredclones, preys, settingsclones[:len(preys)])
    return predArgs, preyArgs

def getResults(predArgs, preyArgs):
    return map(calcscore, predArgs) if len(predArgs) > 1 else [0], map(calcscore, preyArgs) if len(preyArgs) > 1 else [0]

def getMultiProcessedResults(predArgs, preyArgs):
    #Now comes the multiprocessing magic...
    import multiprocessing
    from multiprocessing import Pool
    pool = Pool()
    predResults = pool.map_async(calcscore, predArgs) if len(predArgs) > 1 else None
    preyResults = pool.map_async(calcscore, preyArgs) if len(preyArgs) > 1 else None
    return predResults.get() if predResults else [0], preyResults.get() if preyResults else [0]


def mutate(gens, pred__clones_per_gen, prey_clones_per_gen, settings=DEFAULT_SETTINGS, progress=__printProgress): 
    global best_pred, best_prey, calcscore

    for i in range(gens):
	progress(i, gens)

        preds = [pred for pred in best_pred.getMutations(pred__clones_per_gen)]
        preds.append(best_pred)

        preys =  [prey for prey in best_prey.getMutations(prey_clones_per_gen)]
        preys.append(best_prey)


	predArgs, preyArgs = getCalcScoreArgs(preds, preys, best_pred, best_prey, settings)

	predscores, preyscores = getMultiProcessedResults(predArgs, preyArgs)
	#predscores, preyscores = getResults(predArgs, preyArgs)

	best_prey = preds[predscores.index(max(predscores))]
	best_pred = preys[preyscores.index(max(preyscores))]

	
if __name__ == "__main__":
    gens = input("How many generations?")	
    preds = input("How many predator clones per generation?")	
    preys = input("How many preys clones per generation?")	
    mutate(gens, preds, preys)
    __clearProgress()
    print(best_pred.type)
    print(best_prey.type)
