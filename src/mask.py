import numpy.random
import predpreyalgorithm

def createmask():
    ranges = predpreyalgorithm.getSetting("inputranges")
    inputranges = numpy.array(ranges) + 1 #Ensures that the highest number will occur
    pdfsize = inputranges.prod() * predpreyalgorithm.getSetting("pdfpercent")
    rangecount = len(inputranges)
    choices = predpreyalgorithm.getSetting("choices")
    increment = predpreyalgorithm.getSetting("mutationincrement")

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
            for k,v in mask.iteritems(): print("\t\t%s -> %s" % (k,v))
