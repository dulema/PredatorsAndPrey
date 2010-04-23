import numpy.random

PREDATOR = "predator"
PREY = "prey"

#Give it a set of input sensory data, it outputs a move.
#Naive implementation that currently just runs on python
class Critter:

    def __init__(self, pdfmatrix, type="No type defined", choices = 13):
        self.choices = 13
        self.status = {"hunger":0}
        self.type = ""
        self.type = type
        self.choices = choices
	self.pdfmatrix = pdfmatrix

    #Returns the move to make.
    def getMove(self, senses):
        pdf = self.getHistogram(senses)
        r = numpy.random.random_sample()
        sum = 0
        for i in range(len(pdf)):
            sum = sum + pdf[i]
            if r < sum:
                return i

    def generatePDF(self):
	pdf = numpy.random.random_sample(self.choices)
	pdf /= pdf.sum()
	return pdf
 
    def getHistogram(self, senses):
	input = senses + tuple(self.status.itervalues())
        if input not in self.pdfmatrix:
            self.pdfmatrix[input] = self.generatePDF()
        return self.pdfmatrix[input]

    def getPDFMatrix(self):
        return self.pdfmatrix

    def getStatus(self, name):
        return self.status[name]

    def setStatus(self, name, value):
        self.status[name] = value

    def incrementStatus(self, name, value):
        self.status[name] += value

    def resetStatus(self):
        for key in self.status:
                self.status[key] = 0
        self.status["hunger"] = 0

if __name__ == "__main__":
    s = Critter({}, PREDATOR)
    input = (3, 4, 5)
    s.getMove(input)
#    s.save(open("critters/deniz.predator", "w"))

    c = Critter({}, PREY)
#    c.load(open("critters/deniz.predator", "r"))

    c.setStatus("hunger", c.getStatus("hunger")/2)
    c.getMove((3, 4, 5))
    print("Histogram: %s" % c.getHistogram((3,4,5)))

    print(c.getPDFMatrix())
    #for m in c.getMutations(2, 0.5, (6, 6, 6), 0.3): print(m.pdfmatrix)
    results = [ 0 for _ in range(c.choices)]
    for _ in range(10000):
        r = c.getMove(input)
        results[r] = results[r] + 1
    for x in results: print(x/100.0) 

