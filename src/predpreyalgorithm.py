#Does the work
import mask
import scorealgorithm
import critter

best_pred = {}
best_prey = {}

SIGHT = 20
MAXHUNGER = 20

#These are user definable
DEFAULT_SETTINGS = {"predmutations":4, "preymutations":4, "mutations":10,
                    "sight":20, "mapsize":20,"plantpercent":0.05,
                    "preypercent":0.02, "predpercent":0.01,
                    "plantbites":3, "maxhunger":20,
                    "pdfpercent":0.01,"mutationincrement":0.3,
                    "distancechunks":[3,6,18],
                    "hungerchunks":[3,6,18] }

#Basically input is (preddistance, preddireciton, preydistance, preydirection, vegdistance, vegdirection, hunger)
#Input ranges is the number of different values possible for each entry

DEFAULT_SETTINGS["inputranges"] =( [ len(DEFAULT_SETTINGS["distancechunks"]), 7] * 3 ) + [ len(DEFAULT_SETTINGS["hungerchunks"]) ]
DEFAULT_SETTINGS["choices"] = 7

settings = {}

def getSetting(setting):
    return settings[setting] if setting in settings else DEFAULT_SETTINGS[setting]

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
    return r1.get().append(dry_result), r2.get().append(dry_result)


def MutateAndScore():
    dryrun = createMaskAndScore()
    preds = [createMaskAndScore(critter.PREDATOR) for _ in range(getSetting("predmutations")) ]
    preys = [createMaskAndScore(critter.PREY) for _ in range(getSetting("preymutations")) ]
    preds.append(dryrun)
    preys.append(dryrun)
    return preds, preys


def mutate(gens, settings=DEFAULT_SETTINGS, progress=__printProgress):
    global best_pred, best_prey

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    for i in range(gens):
        progress(i, gens) #Update the progress

        #preds, preys = MultiProcessMutateAndScore(predArgs, preyArgs, settings)
        preds, preys = MutateAndScore()

        #Find the best Pred Mask
        best = 0
        best_pred_mask = {}
        for s, mask in preds:
            if s > best:
                best = s
                best_pred_mask = mask

        #Find the best Prey Mask
        best = 0
        best_prey_mask = {}
        for s, mask in preys:
            if s > best:
                best = s
                best_prey_mask = mask

        #Smash the mask into the best pdf
        for k,v in best_pred_mask.iteritems(): best_pred[k] = v
        for k,v in best_prey_mask.iteritems(): best_prey[k] = v


if __name__ == "__main__":
    gens = input("How many generations would you like calculated?")
    DEFAULT_SETTINGS["predmutations"] = input("How many predator clones per generation?")
    DEFAULT_SETTINGS["preymutations"] = input("How many prey clones per generation?")
    mutate(gens)
    __clearProgress()

