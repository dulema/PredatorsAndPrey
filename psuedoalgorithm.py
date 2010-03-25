generations = 10000
num_of_preds_per_gen = 4
num_of_prey_per_gen = 9

def createFirstPred():
	pass
 
def createFirstPrey():
	pass

best_pred = createFirstPred()
best_prey = createFirstPrey()
         
def createMutations(critter, number):
	critters = []
	for i in range(number):
		critters[i] = critter.mutate()
		return critters
          
def pred_score(pred, prey):
	# Make board 
	# Clone some prey
	# Add pred and pey to the board
	# FIGHT
	# See who won
	# return the score
 
for i in range(generations):
	preds = createMutations(best_pred, num_of_preds_per_gen)
	preds.add(best_pred)
 
	preys = createMutations(best_prey, num_of_prey_per_gen)
	preys.add(best_prey)
 
	score = 0
	tmpbest = null;
	for pred in preds:
		newscore = pred_score(pred, best_prey)
		if newscore > score:
			tmpbestpred = pred

	score = 0       
	for prey in preys:
		newscore = prey_score(prey, best_pred)
		if newscore > score:
			tmpbestpred = prey

	best_pred = tmpbestpred
	best_prey = tmpbestprey
