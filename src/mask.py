import numpy.random
import copy

DEFAULT_MUT_SETTINGS =  [20, 7, 20, 7, 20, 7, 20]

#given a pdf this function will return a number of pdfs that are mutated
def createMasks(args, settings):
    increment = abs(settings["mutationincrement"] if "mutationincrement" in settings else 0.5)
    pdfpercent = settings["pdfpercent"] if "pdfpercent" in settings else 0.5
    inputranges = settings["inputranges"] if "inputranges" in settings else DEFAULT_MUT_SETTINGS
    choices = settings["choices"] if "choices" in settings else 13

    mutationcount = int(pdfpercent*numpy.array(inputranges).prod())

    mapargs = []
    for pdf,howmany in args:
        for _ in range(howmany):
            mapargs.append( (pdf, mutationcount, inputranges, increment, choices) )

    #Single threaded
    results = [createmask(rgs) for rgs in mapargs]

    #Multithreaded
    #results = Pool().map(createmask, mapargs, 20000)

    count = 0
    pdfs = []
    for pdf,howmany in args:
        pdfs.append(results[count : count+howmany])
        count += howmany
    return pdfs


def createmask( x ):
    pdf, pdfsize, ranges, increment, choices  = x
    inputranges = numpy.array(ranges) + 1 #Ensures that the highest number will occur
    rangecount = len(inputranges)
    newpdf = copy.deepcopy(pdf) #Make a new copy of the array to mess with

    mask = {}
    for _ in range(pdfsize):
        random_input = numpy.random.rand(rangecount)
        random_input = (random_input * inputranges).astype(int)

        histogram = numpy.random.rand(choices)
        mask[tuple(random_input)] = histogram / histogram.sum()

    return mask


if __name__ == "__main__":
    pdf1 = {}
    pdf2 = {}

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    result = createMasks( ((pdf1, 5), (pdf2, 3)), {"mutationincrement":0.3, "pdfpercent":0.5, "inputranges":[2, 3, 4] } )
    for n, r in enumerate(result):
        print(" == R %d of %d == "% (n, len(result)))
        for i, x in enumerate(r):
            print("\t == mutation %d ==" % (i))
            for k,v in x.iteritems():
                print("\t\t%s : %s" % (k, v) )
