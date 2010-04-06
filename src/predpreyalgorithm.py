#Does the work
import random
import predpreymap
import copy
import multiprocessing
from multiprocessing import Pool
from critter import Critter


mapsize = 23
plant = 0.5

best_pred = Critter()
best_prey = Critter()

def score(x):
    return (3, 4)



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
	pindex = preyscores.index(bestscore)

	best_prey = preys[pindex]
	best_pred = preds[dindex]
	
if __name__ == "__main__":
    gens = input("How many generations?")	
    preds = input("How many preds per generations?")	
    preys = input("How many preys per generations?")	
    mutate(gens, preds, preys)
    __clearProgress()
    print(best_pred.pdfmatrix)
    print(best_prey.pdfmatrix)
