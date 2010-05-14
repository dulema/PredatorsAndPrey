#Does the work
import mask
import scorealgorithm
import critter
import multiprocessing


best_pred = {}
best_prey = {}

SIGHT = 20
MAXHUNGER = 20

#These are user definable
DEFAULT_SETTINGS = {"predmutations":4, "preymutations":4, "mutations":10,"choices":7,
                    "sight":20, "mapsize":20,"plantpercent":0.05,
                    "preypercent":0.05, "predpercent":0.025,
                    "plantbites":3, "maxhunger":20,
                    "pdfpercent":0.01,"mutationincrement":0.3,
                    "distancechunks":[3,9,18],
                    "hungerchunks":[3,9,18] }


#Basically input is (preddistance, preddireciton, preydistance, preydirection, vegdistance, vegdirection, hunger)
#Input ranges is the number of different values possible for each entry
DEFAULT_SETTINGS["inputranges"] =( [ len(DEFAULT_SETTINGS["distancechunks"]) + 1, 7] * 3 ) + [ len(DEFAULT_SETTINGS["hungerchunks"]) + 1 ]
settings = {}

def getSetting(setting):
    return settings[setting] if setting in settings else DEFAULT_SETTINGS[setting]

def setSetting(setting, value):
    settings[setting] = value

def resetSetting(setting):
    del settings[setting]

def __printProgress(num, total, pred_score, prey_score):
    width = 40
    s = "pred score: %d, prey score %d | %d/%d [" % (pred_score, prey_score, num, total)
    completecount = int((float(num)/total)*40)
    s += completecount * "="
    s +=  (40 - completecount) * "-"
    s += "]\r"
    print s,
    import sys
    sys.stdout.flush()

def __clearProgress():
    print (" "*80) + "\n",
    import sys
    sys.stdout.flush()


def roundprogress(map, score):
        pass
        #print("Progress at %s" % score)
    #   for critter in map.critters: print("%s at %s hunger:%s" % (critter.type, map.critters[critter], critter.getStatus("hunger")))

def getMultiProcessedResults(predArgs, preyArgs):
    #Now comes the multiprocessing magic...
    from multiprocessing import Pool
    pool = Pool()
    predResults = pool.map_async(scorealgorithm.calcscore, predArgs, 20000) if len(predArgs) > 1 else None
    preyResults = pool.map_async(scorealgorithm.calcscore, preyArgs, 20000) if len(preyArgs) > 1 else None
    return predResults.get() if predResults else [0], preyResults.get() if preyResults else [0]

def createMaskAndScore(who=None):
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    if who == critter.PREDATOR:
        m = mask.createmask()
        pred_mask = m
        prey_mask = {}
    elif who == critter.PREY:
        m = mask.createmask()
        pred_mask = {}
        prey_mask = m
    else:
        m = {}
        pred_mask = {}
        prey_mask = {}

    s = scorealgorithm.calcscore(pred_mask, prey_mask)
    return s, m

def MultiThreadedMutateAndScore():
    from multiprocessing import Pool
    p = Pool()
    r0 = p.apply_async(createMaskAndScore)
    r1 = p.map_async(createMaskAndScore, [critter.PREDATOR] * getSetting("predmutations") )
    r2 = p.map_async(createMaskAndScore, [critter.PREY] * getSetting("preymutations") )
    dry_result = r0.get()
    preds = r1.get()
    preds.append(dry_result)
    preys = r2.get()
    preys.append(dry_result)
    return preds, preys


def MutateAndScore():
    dryrun = createMaskAndScore()
    preds = [createMaskAndScore(critter.PREDATOR) for _ in range(getSetting("predmutations")) ]
    preys = [createMaskAndScore(critter.PREY) for _ in range(getSetting("preymutations")) ]
    preds.append(dryrun)
    preys.append(dryrun)
    return preds, preys

def getTupleMax(tuplelist):
    scores = zip(*tuplelist)[0]
    return tuplelist[scores.index(max(scores))]


if multiprocessing.cpu_count() == 1:
    mutate_and_score = MutateAndScore
else:
    mutate_and_score = MultiThreadedMutateAndScore


def mutate(gens, settings=DEFAULT_SETTINGS, progress=__printProgress):
    global best_pred, best_prey

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    best_pred_score = 0
    best_prey_score = 0
    for i in range(gens):
        progress(i, gens, best_pred_score, best_prey_score) #Update the progress

        preds, preys = mutate_and_score()

        #Find the best masks
        best_pred_score, best_pred_mask = getTupleMax(preds)
        best_prey_score, best_prey_mask = getTupleMax(preys)

        #Smash the mask into the best pdf
        for k,v in best_pred_mask.iteritems(): best_pred[k] = v
        for k,v in best_prey_mask.iteritems(): best_prey[k] = v
    progress(gens,gens, best_pred_score, best_prey_score)#deniz was here

if __name__ == "__main__":
    gens = input("How many generations would you like calculated?")
    DEFAULT_SETTINGS["predmutations"] = input("How many predator clones per generation?")
    DEFAULT_SETTINGS["preymutations"] = input("How many prey clones per generation?")
    mutate(gens)
    import pickle
    preyf = file("best_prey.prey", "w")
    pickle.dump(best_prey, preyf)
    predf = file("best_pred.pred", "w")
    pickle.dump(best_pred, predf)
    __clearProgress()

