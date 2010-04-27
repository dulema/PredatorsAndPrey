import multiprocessing
import numpy.random

#given a pdf this function will return a number of pdfs that are mutated
def createMasks(howmany, settings):

    increment = settings["mutationincrement"]
    pdfpercent = settings["pdfpercent"]
    inputranges = settings["inputranges"]
    choices = settings["choices"]
    mutationcount = int(pdfpercent*numpy.array(inputranges).prod())

    mapargs = []
    for _ in range(howmany):
        mapargs.append( (mutationcount, inputranges, increment, choices) )

    #Single threaded
    results = [createmask(rgs) for rgs in mapargs]

    #Multithreaded
    results = multiprocessing.Pool().map(createmask, mapargs)

    return results


def createmask( x ):
    pdfsize, ranges, increment, choices  = x
    inputranges = numpy.array(ranges) + 1 #Ensures that the highest number will occur
    rangecount = len(inputranges)

    #Generate the random input
    random_inputs = (numpy.random.random((pdfsize, rangecount))*inputranges).astype(numpy.uint8)
    #Generate the historgrams to go with them
    histograms = numpy.random.random_integers(low=1,high=255,size=(7,pdfsize)).astype(numpy.uint8)

    mask = {}
    for ri,histogram in zip(random_inputs, histograms):
        mask[tuple(ri)] = histogram

    return mask


if __name__ == "__main__":

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    rounds = 10
    settings = {"mutationincrement":0.3, "pdfpercent":0.01, "inputranges":[5, 70, 2], "choices":7 }
    for i in range(rounds):
        print(" ==== ROUND %d ====" % i)
        for i, mask in enumerate(createMasks(5, settings)):
            print("\t === Mask %d ===" % i)
            print mask

#    for n, r in enumerate(result):
#        print(" == R %d of %d == "% (n, len(result)))
#        for i, x in enumerate(r):
#            print("\t == mutation %d ==" % (i))
#            for k,v in x.iteritems():
#                print("\t\t%s : %s" % (k, v) )
