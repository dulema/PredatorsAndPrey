import numpy
import pickle
import itertools

histogram = numpy.array([0, 0, 0, 255, 0, 0, 0], dtype=numpy.uint8)
allinputs = itertools.product(range(4), range(7),range(4), range(7),range(4), range(7), range(4))
pdf = {}
for input in allinputs:
    print input
    pdf[input] = histogram.copy()
print(histogram)
pickle.dump(pdf, file("fixedpdf.pred", "w"))
