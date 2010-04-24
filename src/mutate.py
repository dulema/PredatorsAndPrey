import numpy.random
import copy
import multiprocessing
from multiprocessing import Pool

try:
    import psyco
    psyco.full()
except ImportError:
    pass

DEFAULT_MUT_SETTINGS =  [20, 7, 20, 7, 20, 7, 20]

#given a pdf this function will return a number of pdfs that are mutated
def createMutations(args, settings):
    increment = abs(settings["mutationincrement"] if "mutationincrement" in settings else 0.5)
    pdfpercent = settings["pdfpercent"] if "pdfpercent" in settings else 0.5
    inputranges = settings["inputranges"] if "inputranges" in settings else DEFAULT_MUT_SETTINGS

    mutationcount = int(pdfpercent*numpy.array(inputranges).prod())

    mapargs = []
    for pdf,howmany in args:
        for _ in range(howmany):
            mapargs.append( (pdf, mutationcount, inputranges, increment) )

    #Single threaded
    results = map(mutatepdf, mapargs)

    #Multithreaded
    #results = Pool().map(mutatepdf, mapargs, 20000)

    count = 0
    pdfs = []
    for pdf,howmany in args:
        pdfs.append(results[count:count + howmany])
        count += howmany
    return pdfs


def mutatepdf( x ):
    pdf, pdfsize, ranges, increment  = x

    inputranges = numpy.array(ranges) + 1 #Ensures that the highest number will occur

    newpdf = copy.deepcopy(pdf) #Make a new copy of the array to mess with
    increments = numpy.random.uniform(-increment, increment, pdfsize) #Generate all of the random increments to be added to the pdfs
    inputs = (numpy.random.uniform(0, 1, (pdfsize, len(inputranges))) * inputranges).astype('int') #generate all of the random inputs in one fell swoop

    for i, rand in enumerate(inputs):
        randominput = tuple(rand)
        if randominput not in newpdf:
            hist = numpy.random.random_sample(len(inputranges))
            hist /= hist.sum()
            newpdf[randominput] = hist

        hist = newpdf[randominput] #Get the histogram for a move
        randommove = numpy.random.randint(0,len(hist)) #pick a random move to change
        hist[randommove] += increments[i] #Randomly modify the histogram
        hist[randommove] = abs(hist[randommove])
        hist /= hist.sum() #Normalize the vector by dividing by the sum of the elements
    return newpdf



if __name__ == "__main__":
    pdf1 = {}
    pdf2 = {}

    result = createMutations( ((pdf1, 5), (pdf2, 3)), {"mutationincrement":0.3, "pdfpercent":0.5, "inputranges":[2, 3, 4] } )
    for n, r in enumerate(result):
        print(" == R %d of %d == "% (n, len(result)))
        for i, x in enumerate(r):
            print("\t == mutation %d ==" % (i))
            for k,v in x.iteritems():
                print("\t\t%s : %s" % (k, v) )
