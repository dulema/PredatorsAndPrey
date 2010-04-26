import numpy.random

DEFAULT_MUT_SETTINGS =  [20, 7, 20, 7, 20, 7, 20]

#given a pdf this function will return a number of pdfs that are mutated
def createMasks(howmany, settings):

    increment = abs(settings["mutationincrement"] if "mutationincrement" in settings else 0.5)
    pdfpercent = settings["pdfpercent"] if "pdfpercent" in settings else 0.5
    inputranges = settings["inputranges"] if "inputranges" in settings else DEFAULT_MUT_SETTINGS
    choices = settings["choices"] if "choices" in settings else 13
    mutationcount = int(pdfpercent*numpy.array(inputranges).prod())

    mapargs = []
    for _ in range(howmany):
        mapargs.append( (mutationcount, inputranges, increment, choices) )

    #Single threaded
    results = [createmask(rgs) for rgs in mapargs]

    #Multithreaded
    #results = Pool().map(createmask, mapargs, 20000)

    return results


def createmask( x ):
#    import time
#    start_create = time.time()
    pdfsize, ranges, increment, choices  = x
    inputranges = numpy.array(ranges) + 1 #Ensures that the highest number will occur
    rangecount = len(inputranges)

    #Generate the random input
#    start_random = time.time()
    random_inputs = numpy.column_stack([numpy.random.randint(low=0,high=lim,size=(pdfsize)) for lim in inputranges])
#    input_time = time.time() - start_random

    #Generate the historgrams to go with them
#    hist_start = time.time()
    histograms = numpy.random.uniform(low=0,high=1.0,size=(13,pdfsize))
    s = numpy.reciprocal(histograms.sum(0))
    histograms *= s
#    histo_time = time.time() - hist_start

    mask = {}
    for ri,histogram in zip(random_inputs, histograms):
        mask[tuple(ri)] = histogram

#    random_time = time.time() - start_random
 #   total_time = time.time() - start_create
#    print("For %d pdfs the total time is: %d seconds, %d (%d%%) of which where spent in random" % (pdfsize, total_time, random_time, int((random_time/float(total_time))*100) ))
#    print("\t%d seconds (%d%%) spent for inputs\n\t%d seconds (%d%%) spent for histograms" % (input_time, int((float(input_time)/random_time)*100) , histo_time, int((float(histo_time)/random_time)*100) ))
    return mask


if __name__ == "__main__":

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    rounds = 10
    settings = {"mutationincrement":0.3, "pdfpercent":0.01, "inputranges":[20, 7, 20, 7, 20, 7, 20], "choices":13 }
    for i in range(rounds):
        print(" ==== ROUND %d ====" % i)
        createMasks(5, settings)

#    for n, r in enumerate(result):
#        print(" == R %d of %d == "% (n, len(result)))
#        for i, x in enumerate(r):
#            print("\t == mutation %d ==" % (i))
#            for k,v in x.iteritems():
#                print("\t\t%s : %s" % (k, v) )
