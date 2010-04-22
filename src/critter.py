import random
import copy

PREDATOR = "predator"
PREY = "prey"

#Give it a set of input sensory data, it outputs a move.
#Naive implementation that currently just runs on python
class Critter:

    def __init__(self, type="No type defined", choices = 13):
        self.pdfmatrix = {}
        self.choices = 13
        self.status = {"hunger":0}
        self.type = ""
        self.type = type
        self.choices = choices

    #Returns the move to make.
    def getMove(self, senses):
        pdf = self.getHistogram(senses)
        r = random.random()
        sum = 0
        for i in range(len(pdf)):
            sum = sum + pdf[i]
            if r < sum:
                return i

    def generatePDF(self):
        pdf = [ random.randint(1, 10) for _ in range(self.choices) ]
        total = sum(pdf)
        return [float(i)/total for i in pdf]
 
    def getHistogram(self, senses):
        s = [x for x in senses]
        for x in self.status.itervalues(): s.append(x)
        input = tuple(s)
        if input not in self.pdfmatrix:
            self.pdfmatrix[input] = self.generatePDF()
        return self.pdfmatrix[input]

    def getPDFMatrix(self):
        return self.pdfmatrix

    def clone(self, howmany):
        for _ in range(howmany):
                yield copy.deepcopy(self)
    
    def getMutations(self, howmany):
        for c in self.clone(howmany):
            c.mutate()
            yield c


    def mutate(self, percentpdf, inputranges, increment):
        if not self.pdfmatrix: #just quit if we don't have any entries
                return

	#The size of the pdf matrix is the product of the ranges
	for _ in range(percentpdf*reduce(lambda x,y:x*y, inputranges)):
		randominput = map(lambda x:random.randint(0, x), inputranges)


        key = random.choice([k for k in iter(self.pdfmatrix)]) 
        pdf = self.pdfmatrix[key]
        index = random.randrange(len(pdf))
        pdf[index] = pdf[index] + random.uniform(-increment, increment)
        normalizer = sum(pdf)
        self.pdfmatrix[key] = [float(i)/normalizer for i in pdf]

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

    # No pickling the files yet, nice to be able to read the data without the program
    def save(self, file):
        file.write(self.type + "\n") 
        file.write(str(self.pdfmatrix) + "\n")
        file.write(str(self.choices))
        file.close()

    def load(self, file):
        type = file.readline()
        stringmatrix = file.readline()
        choices = file.readline()
        file.close()
        self.pdfmatrix = type
        self.pdfmatrix = eval(stringmatrix)
        self.choices = eval(choices)

if __name__ == "__main__":
    s = Critter("Predator")
    input = (3, 4, 5)
    s.getMove(input)
    s.save(open("critters/deniz.predator", "w"))

    c = Critter()
    c.load(open("critters/deniz.predator", "r"))

    c.setStatus("hunger", c.getStatus("hunger")/2)
    c.getMove((3, 4, 5))
    print("Histogram: %s" % c.getHistogram((3,4,5)))

    print(c.getPDFMatrix())
    for m in c.getMutations(2): print(m.pdfmatrix)
    results = [ 0 for _ in range(c.choices)]
    for _ in range(10000):
        r = c.getMove(input)
        results[r] = results[r] + 1
    for x in results: print(x/100.0) 

