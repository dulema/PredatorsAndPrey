#Does the work
import random
import map

mapsize = 23
plant = 0.5

predcount = 3
preycount = 10

def createDefaultPredStatus():
    return {"hunger":100, "sleepiness":100, "isalive":true}

def createDefaultPreyStatus():
    return {"hunger":100, "sleepiness":100, "isalive":true}

best_pred = ({"hungervotes":1, "grouping":1, "fatigue":1}, createDefaultPredStatus())
best_prey =({"hungervotes":1, "fearvotes":1, "grouping":1, "fatigue":1}, createDefaultPreyStatus()) 

def mutateBehavior(critter):
	behavior = critter[0]
	mutation = {}
	for key in iter(behavior):
		mutation[key] = behavior[key] + (random.randint(-3, 3))
		while mutation[key] < 1:
			mutation[key] = behavior[key] + (random.randint(-3, 3))
	return mutation 
         
def createPreyMutation(prey, number):
	for i in range(number):
		yield (mutateBehavior(prey), createDefaultPreyStatus()) 

def createPredatorMutation(predator, number):
	for i in range(number):
		yield (mutateBehavior(predator), createDefaultPredStatus())
		
def score(pred, prey):
    	global mapsize, plant, predcount, preycount
    	map = map.Map(mapsize, plant)

	preds = []
	for i in range(predcount):
	    tpred = (pred[0], createDefaultPredStatus())
	    map.setCritterAt(map.getRandomUntakenTile(), tpred) 
	    preds.append(tpred)

	preys = []
	for i in range(preycount):
	    tprey = (prey[0], createDefaultPreyStatus())
	    map.setCritterAt(map.getRandomUntakenTile(),tprey) 
	    preys.append(tprey)

	#This is a totally horrible way to do this
	days = 0
	while len(preys) != 0 and len(preds) != 0:
	    days = days + 1
	    for p in preys:
		map.moveCritter(p, ai.getPreyNextMove(map, p))

	    for p in preds:
		map.moveCritter(p, ai.getPredatorNextMove(map, p))
	
	    preys = filter(lambda x : x[1]["isalive"], preys)
	    preds = filter(lambda x : x[1]["isalive"], preds)

	return days 

def mutate(gens, num_of_preds_per_gen, num_of_prey_per_gen): 
    global best_pred, best_prey
    for i in range(gens):
	    preds = [pred for pred in createPredatorMutation(best_pred, num_of_preds_per_gen - 1)]
	    preds.append(best_pred)
     
	    preys = [prey for prey in createPreyMutation(best_prey, num_of_prey_per_gen - 1)]
	    preys.append(best_prey)
     
	    currentscore = 0
	    for pred in preds:
		    newscore = score(pred, best_prey)
		    if newscore > currentscore:
			    currentscore = newscore
			    tmpbestpred = pred

	    currentscore = 0       
	    for prey in preys:
		    newscore = score(best_pred, prey)
		    if newscore > currentscore:
			    currentscore = newscore
			    tmpbestprey = prey

	    best_pred = tmpbestpred
	    best_prey = tmpbestprey
