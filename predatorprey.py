#Does the work
import random

generations = input("How many generations would you like this to run for?")
num_of_preds_per_gen = input("How many predators would you like per generation?")
num_of_prey_per_gen =  input("How many prey would you like per generation?")

def createDefaultPredStatus():
	return {"hunger":100, "sleepiness":100}

def createDefaultPreyStatus():
	return {"hunger":100, "sleepiness":100}

def createFirstPred():
	return ({"hungervotes":1, "grouping":1, "fatigue":1}, createDefaultPredStatus())
 
def createFirstPrey():
	return ({"hungervotes":1, "fearvotes":1, "grouping":1, "fatigue":1}, createDefaultPreyStatus())

best_pred = createFirstPred()
best_prey = createFirstPrey()

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
	return (sum([pred[0][key] for key in pred[0]]),sum([prey[0][key] for key in prey[0]])) 
 
for i in range(generations):
	preds = [pred for pred in createPredatorMutation(best_pred, num_of_preds_per_gen - 1)]
	preds.append(best_pred)
 
	preys = [prey for prey in createPreyMutation(best_prey, num_of_prey_per_gen - 1)]
	preys.append(best_prey)
 
	currentscore = 0
	for pred in preds:
		newscore = score(pred, best_prey)[0]
		if newscore > currentscore:
			currentscore = newscore
			tmpbestpred = pred

	currentscore = 0       
	for prey in preys:
		newscore = score(best_pred, prey)[1]
		if newscore > currentscore:
			currentscore = newscore
			tmpbestprey = prey

	best_pred = tmpbestpred
	best_prey = tmpbestprey

print(best_pred[0])
print(best_prey[0])
