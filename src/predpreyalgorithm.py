#Does the work
from predpreymap import Map
import critter
from critter import Critter
import mask
import scorealgorithm

best_pred = {}
best_prey = {}

DEFAULT_SETTINGS = {"mapsize":20, "vegpercent":0.05, "preypercent":0.02, "predpercent":0.01, "sight":10, "plantbites":3, "maxhunger":20, "pdfpercent":0.01, "inputranges":(10,7,10,7,10,7,20), "mutationincrement":0.3}


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
    return map(scorealgorithm.calcscore, predArgs) if len(predArgs) > 1 else [0], map(scorealgorithm.calcscore, preyArgs) if len(preyArgs) > 1 else [0]

def getMultiProcessedResults(predArgs, preyArgs):
    #Now comes the multiprocessing magic...
    import multiprocessing
    from multiprocessing import Pool
    pool = Pool()
    predResults = pool.map_async(scorealgorithm.calcscore, predArgs, 20000) if len(predArgs) > 1 else None
    preyResults = pool.map_async(scorealgorithm.calcscore, preyArgs, 20000) if len(preyArgs) > 1 else None
    return predResults.get() if predResults else [0], preyResults.get() if preyResults else [0]


def mutate(gens, pred_clones_per_gen, prey_clones_per_gen, settings=DEFAULT_SETTINGS, progress=__printProgress): 
    global best_pred, best_prey

    try:
        import psyco
        psyco.log()
        psyco.full()
        psyco.profile(0.05, memory=100)
        psyco.profile(0.2)
    except ImportError:
        pass

    for i in range(gens):
        progress(i, gens) #Update the progress

        #creats the masks. Masks hold the difference between the original critter and the new mutated one.
        predmasks, preymasks = mask.createMasks(((best_pred, pred_clones_per_gen), (best_prey, prey_clones_per_gen)), settings)

        predmasks.append({}) #This is how we add the best_pred to the mix. The best_pred has an empty mask
        preymasks.append({}) #This is how we add the best_prey to the mix. The best_prey has an empty mask

        predArgs, preyArgs = getCalcScoreArgs(predmasks, preymasks, best_pred, best_prey, settings)

        #predpdfscores, preypdfscores = getMultiProcessedResults(predArgs, preyArgs)
        predscores, preyscores = getResults(predArgs, preyArgs)

        #Pickout the best mask
        best_pred_mask = predmasks[predscores.index(max(predscores))]
        best_prey_mask = preymasks[preyscores.index(max(preyscores))]

        #Merge the mask into the best pdf
        for k,v in best_pred_mask.iteritems(): best_pred[k] = v
        for k,v in best_prey_mask.iteritems(): best_prey[k] = v


if __name__ == "__main__":
    gens = input("How many generations?")
    preds = input("How many predator clones per generation?")
    preys = input("How many preys clones per generation?")
    mutate(gens, preds, preys)
    __clearProgress()
