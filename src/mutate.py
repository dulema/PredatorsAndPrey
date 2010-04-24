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
    newpdf = pdf
    increment = abs(settings["mutationincrement"] if "mutationincrement" in settings else 0.5)
    pdfpercent = settings["pdfpercent"] if "pdfpercent" in settings else 0.5
    inputranges = settings["inputranges"] if "inputranges" in settings else DEFAULT_MUT_SETTINGS

    mutationcount = int(pdfpercent*numpy.array(inputranges).prod())

    mapargs = ()
    for pdf,howmany in args:
        mapargs += (pdf, mutationcount, inputranges) * howmany

    mutations = []
    increments = numpy.random.uniform(-increment, increment, pdfsize * howmany)

def mutatepdf( x ):
    pdf, pdfsize, inputranges  = x

    newpdf = copy.deepcopy(pdf)
    for i in range(pdfsize):
        randominput = tuple(map(lambda x:numpy.random.random_integers(x), inputranges))
        if randominput not in pdf:
            hist = numpy.random.random_sample(len(inputranges))
            hist /= hist.sum()
            pdf[randominput] = hist

        hist = pdf[randominput] #Get the histogram for a move
        randommove = numpy.random.randint(0,len(hist)) #pick a random move to change
        hist[randommove] += increments[ (j*pdfsize) + i] #Randomly modify the histogram
        hist /= hist.sum() #Normalize the vector by dividing by the sum of the elements
    mutations.append(newpdf)
    return mutations
