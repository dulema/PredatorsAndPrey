import numpy.random
import predpreyalgorithm

def createmask():
    ranges = predpreyalgorithm.getSetting("inputranges")
    inputranges = numpy.array(ranges) #Ensures that the highest number will occur
    pdfsize = int(inputranges.prod() * predpreyalgorithm.getSetting("pdfpercent"))
    rangecount = len(inputranges)
    choices = predpreyalgorithm.getSetting("choices")
    increment = predpreyalgorithm.getSetting("mutationincrement")

    #Generate the random input
    random_inputs = (numpy.random.random((pdfsize, rangecount))*inputranges).astype(numpy.uint8)
    #Generate the historgrams to go with them
    histograms = numpy.random.random_integers(low=1,high=255,size=(pdfsize,7)).astype(numpy.uint8)

    #print("Number of histograms: %d "% len(histograms) )
    #print("Entry count: %d" % len(histograms[0]))

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

    print("Settings are: %s\n" % predpreyalgorithm.DEFAULT_SETTINGS)

    rounds = 10
    for i in range(rounds):
        print(" ==== ROUND %d ====" % i)
        mask = createmask()
        for k,v in mask.iteritems(): print("\t\t%s -> %s" % (k,v))
