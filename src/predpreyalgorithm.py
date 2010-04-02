#Does the work
import random
import predpreymap
from multiprocessing import Pool

mapsize = 23
plant = 0.5

predcount = 3
preycount = 10

def getDefaultPreds(num):
    for _ in range(num):
	yield createDefaultPredStatus();

def getDefaultPreys(num):
    for _ in range(num):
	yield createDefaultPreyStatus();

best_pred = {"hungervotes":1, "grouping":1, "fatigue":1}
best_prey = {"hungervotes":1, "fearvotes":1, "grouping":1, "fatigue":1}

def mutateBehavior(critter):
    mutation = {}
    for key in iter(critter):
	    mutation[key] = critter[key] + (random.randint(-3, 3))
	    while mutation[key] < 1:
		    mutation[key] = critter[key] + (random.randint(-3, 3))
    return mutation 
         
def createPreyMutation(prey, number):
	for i in range(number):
		yield mutateBehavior(prey) 

def createPredatorMutation(predator, number):
	for i in range(number):
		yield mutateBehavior(predator)
		
def score(pred, prey):
    return sum( [pred[i] for i in iter(pred)] )


#    	global mapsize, plant, predcount, preycount
#    	map = map.Map(mapsize, plant)
#
#    	preds = []
#	for i in range(predcount):
#	    tpred = (pred[0], createDefaultPredStatus())
#	    map.setCritterAt(map.getRandomUntakenTile(), tpred) 
#	    preds.append(tpred)
#
#	preys = []
#	for i in range(preycount):
#	    prey = (prey[0], createDefaultPreyStatus())
#	    map.setCritterAt(map.getRandomUntakenTile(),tprey) 
#	    preys.append(tprey)
#
	#This is a totally horrible way to do this
#	days = 0
#	while len(preys) != 0 and len(preds) != 0:
#	    days = days + 1
#	    for p in preys:
#		map.moveCritter(p, ai.getPreyNextMove(map, p))
#
#	    for p in preds:
#		map.moveCritter(p, ai.getPredatorNextMove(map, p))
#	
#	    preys = filter(lambda x : x[1]["isalive"], preys)
#	    preds = filter(lambda x : x[1]["isalive"], preds)
#
#	return days 


def mutate(gens, num_of_preds_per_gen, num_of_prey_per_gen): 
    global best_pred, best_prey, score
    for _ in range(gens):

	preds = [pred for pred in createPredatorMutation(best_pred, num_of_preds_per_gen - 1)]
	preds.append(best_pred)

	preys =  [prey for prey in createPreyMutation(best_prey, num_of_prey_per_gen - 1)]
	preys.append(best_prey)

 
#	Generate a Pool of processes to run all of the scoring for the predators
#	predPool = Pool(processes=len(preds))
#	predResult = predPool.map_async(score, zip(preds, [best_prey for _ in range(len(preds))]) )


#	preyPool = Pool(processes=len(preys))
#	preyResult = preyPool.map_async(score, zip([best_pred for _ in range(len(preys))], preys ))
	

	#Parse the results
#	predscores = predResult.get(None) #Probably dangerous to not specify a timeout
	predscores = map( score, preds, [best_prey for _ in range(num_of_preds_per_gen)])
	bestscore = max(predscores)
	dindex = predscores.index(bestscore)

#	preyscores = preyResult.get(None)
	preyscores = map ( score, [best_pred for _ in range(len(preys))], preys )
	bestscore = max(preyscores)
	pindex = preyscores.index(bestscore)

	best_prey = preys[pindex]
	best_pred = preds[dindex]
	
if __name__ == "__main__":
    gens = input("How many generations?")	
    preds = input("How many preds per generations?")	
    preys = input("How many preys per generations?")	
    mutate(gens, preds, preys)
    print(best_pred)
    print(best_prey)
