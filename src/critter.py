import numpy

PREDATOR = "predator"
PREY = "prey"

#Give it a set of input sensory data, it outputs a move.
#Naive implementation that currently just runs on python
class Critter:

    def __init__(self, pdfmatrix, mask, type="No type defined", choices = 13):
        self.choices = 13
        self.status = {"hunger":0}
        self.type = ""
        self.type = type
        self.choices = choices
        self.pdfmatrix = pdfmatrix
        self.mask = mask

    #
    # Given a set of inputs this function will return
    # All of the moves that should be attemped in the
    # order that they should be attempted
    #
    def getMoves(self, senses):
        pdf = self.getHistogram(senses).copy()
        moves = []
        while len(pdf) > 0: #Keep going until the pdf is empty
            r = numpy.random.uniform() #Pick a random number [0,1)
            sum = 0 #Track how high we are
            for i,probability in enumerate(pdf): #For every i from 0 -> len(pdf) and every probability in the pdf
                sum += probability
                if r < sum:
                    moves.append(i)
                    numpy.delete(pdf, i) #remove this option from the pdf
                    pdf /= pdf.sum() #Renormalize the pdf
                    break
        return moves

    def generatePDF(self):
        pdf = numpy.random.random_sample(self.choices)
        pdf /= pdf.sum()
        return pdf

    def getHistogram(self, senses):
        input = senses + tuple(self.status.itervalues())
        if input not in self.mask:
            if input not in self.pdfmatrix:
                pdf = self.generatePDF()
                self.pdfmatrix[input] = pdf
                return pdf
            else:
                return self.pdfmatrix[input]
        else:
            return self.mask[input]

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
    s = Critter({},{}, PREDATOR)
    input = (3, 4, 5)
    s.getMove(input)
#    s.save(open("critters/deniz.predator", "w"))

    c = Critter({}, {}, PREY)
#    c.load(open("critters/deniz.predator", "r"))

    c.setStatus("hunger", c.getStatus("hunger")/2)
    c.getMove((3, 4, 5))
    print("Histogram: %s" % c.getHistogram((3,4,5)))

    #for m in c.getMutations(2, 0.5, (6, 6, 6), 0.3): print(m.pdfmatrix)
    results = [ 0 for _ in range(c.choices)]
    for _ in range(10000):
        r = c.getMove(input)
        results[r] = results[r] + 1
    for x in results: print(x/100.0) 

