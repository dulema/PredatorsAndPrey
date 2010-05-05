import numpy
import pickle
import itertools

filename = raw_input("File name to save this critter?")
hist = raw_input("What histogram would you like this to be? [Please, seven (7) entries that are between 0-255, deliminated by commas]")
histo = map(lambda x : int(x), hist.split(","))
print("The following histogram will be used for every input: %s" % histo)

histogram = numpy.array(histo, dtype=numpy.uint8)
allinputs = itertools.product(range(4), range(7),range(4), range(7),range(4), range(7), range(4))

pdf = {}
for input in allinputs:
    pdf[input] = histogram.copy()
print(histogram)
pickle.dump(pdf, file(filename, "w"))
