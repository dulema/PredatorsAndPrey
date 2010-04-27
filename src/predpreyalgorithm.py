#Does the work
import mask
import scorealgorithm

best_pred = {}
best_prey = {}

SIGHT = 20
MAXHUNGER = 20

DEFAULT_SETTINGS = {"sight":20, "mapsize":20,"plantpercent":0.05,
                    "preypercent":0.02, "predpercent":0.01,
                    "plantbites":3, "maxhunger":20,
                    "pdfpercent":0.01,"muttionincrement":0.3,
                    "distancechunks":[3,6,18],
                    "hungerchunks":[3,6,18] }

#Basically input is (preddistance, preddireciton, preydistance, preydirection, vegdistance, vegdirection, hunger)
#Input ranges is the number of different values possible for each entry

DEFAULT_SETTINGS["inputranges"] =( [ len(DEFAULT_SETTINGS["distancechunks"]), 7] * 3 ) + [ len(DEFAULT_SETTINGS["hungerchunks"]) ]

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


def getCalcScoreArgs(preds, preys, bpred, bprey, settings):
    bpreyclones = [ (bprey, {}) for _ in preds]
    bpredclones = [ (bpred, {}) for _ in preys]
    settingsclones = [settings] * max(len(preds),len(preys))
    preds = zip( [bpred]*len(preds), preds)
    preys = zip( [bprey]*len(preys), preys)
    predArgs = zip( preds, bpreyclones, settingsclones[:len(preds)])
    preyArgs = zip(bpredclones, preys, settingsclones[:len(preys)])
    return predArgs, preyArgs

def getResults(predArgs, preyArgs):
    predResults = [0]
    preyResults = [0]

    if len(predArgs) > 1:
        predResults = [ scorealgorithm.calcscore(arg) for arg in predArgs ]

    if len(preyArgs) > 1:
        preyResults = [ scorealgorithm.calcscore(arg) for arg in preyArgs ]

    return predResults, preyResults

def getMultiProcessedResults(predArgs, preyArgs):
    #Now comes the multiprocessing magic...
    from multiprocessing import Pool
    pool = Pool()
    predResults = pool.map_async(scorealgorithm.calcscore, predArgs, 20000) if len(predArgs) > 1 else None
    preyResults = pool.map_async(scorealgorithm.calcscore, preyArgs, 20000) if len(preyArgs) > 1 else None
    return predResults.get() if predResults else [0], preyResults.get() if preyResults else [0]


def mutate(gens, pred_clones_per_gen, prey_clones_per_gen, settings=DEFAULT_SETTINGS, progress=__printProgress): 
    global best_pred, best_prey


    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    import time
    mask_times = []
    score_times = []
    gen_time = []
    start = time.time()

    for i in range(gens):
        gen_start = time.time()
        progress(i, gens) #Update the progress

        mask_start = time.time()
        #creats the masks. Masks hold the difference between the original critter and the new mutated one.
        masks = mask.createMasks(pred_clones_per_gen+prey_clones_per_gen, settings)
        predmasks = masks[:pred_clones_per_gen]
        predmasks.append({}) #This is how we add the best_pred to the mix. The best_pred has an empty mask
        preymasks = masks[pred_clones_per_gen:]
        preymasks.append({}) #This is how we add the best_prey to the mix. The best_prey has an empty mask
        mask_times.append(time.time() - mask_start)

        score_start = time.time()
        predArgs, preyArgs = getCalcScoreArgs(predmasks, preymasks, best_pred, best_prey, settings)
        predscores, preyscores = getMultiProcessedResults(predArgs, preyArgs)
        #predscores, preyscores = getResults(predArgs, preyArgs)
        score_times.append(time.time() - score_start)

        #Pickout the best mask
        best_pred_mask = predmasks[predscores.index(max(predscores))]
        best_prey_mask = preymasks[preyscores.index(max(preyscores))]

        #Merge the mask into the best pdf
        for k,v in best_pred_mask.iteritems(): best_pred[k] = v
        for k,v in best_prey_mask.iteritems(): best_prey[k] = v
        gen_time.append(time.time() - gen_start)

    end = time.time()
    totaltime = sum(gen_time)
    print("\nTotal time: %d" % (totaltime) )
    for i,masktime,scoretime,gentime in zip(range(gens), mask_times, score_times,gen_time):
        print("\tGeneration %d took %d%% of the total time" % (i, int( (gentime/totaltime)*100 )))
        print("\t\tMasking took %d%% of the total generation time" % (int( (masktime/float(gentime))* 100 )) )
        print("\t\tScoring took %d%% of the total generation time" % (int( (scoretime/float(gentime))* 100 )) )

    print("In total: ")
    print("\tMasking took %d%% of the time" % int( (sum(mask_times) / float(totaltime)) * 100 ) )
    print("\tScoring took %d%% of the time" % int( (sum(score_times) / float(totaltime)) * 100 ) )


if __name__ == "__main__":
    gens = input("How many generations?")
    preds = input("How many predator clones per generation?")
    preys = input("How many preys clones per generation?")
    mutate(gens, preds, preys)
    __clearProgress()
