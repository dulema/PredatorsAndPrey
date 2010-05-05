import numpy
import pickle
import itertools

histogram = numpy.array([0, 0, 0, 255, 0, 0, 0])
allinputs = itertools.product(range(4), range(7),range(4), range(7),range(4), range(7), range(4))
pdf = {}
for input in allinputs:
    pdf[input] = histogram.copy()

pickle.dump(pdf, file("fixedpdf.pred", "w"))
