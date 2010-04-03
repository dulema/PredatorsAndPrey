import random
import copy

#Give it a set of input sensory data, it outputs a move.
#Naive implementation that currently just runs on python
class Critter:

    pdfmatrix = {}
    choices = 6

    #Returns the move to make.
    def getMove(self, input):
	if not input in self.pdfmatrix:
	    self.pdfmatrix[input] = self.generatePDF() 
	    
	r = random.random()
	pdf = self.pdfmatrix[input]
	sum = 0
	for i in range(len(pdf)):
	    sum = sum + pdf[i]
	    if r < sum:
		return i
   
    def generatePDF(self):
	pdf = [ random.randint(1, 10) for _ in range(self.choices) ]
	total = sum(pdf)
	return [float(i)/total for i in pdf]

    def getPDFMatrix(self):
	return self.pdfmatrix

    def getMutations(self, howmany):
	for _ in range(howmany):
	    c = Critter()
	    #Can't use pdfmatrix.copy() because that only creates a shallow copy.
	    c.pdfmatrix = copy.deepcopy(self.pdfmatrix) 
	    c.mutate()
	    yield c

    def mutate(self):
	pass

    # No pickling the files yet, nice to be able to read the data without the program
    def save(self, file):
	file.write(str(self.pdfmatrix) + "\n")
	file.write(str(self.choices))
	file.close()

    def load(self, file):
	stringmatrix = file.readline()
	choices = file.readline()
	file.close()
	self.pdfmatrix = eval(stringmatrix)
	self.choices = eval(choices)


if __name__ == "__main__":
    s = Critter()
    input = (3, 4, 5)
    s.getMove(input)
    s.save(open("sandrotest", "w"))

    c = Critter()
    c.load(open("sandrotest", "r"))

    print(c.getPDFMatrix())
    results = [ 0 for _ in range(c.choices)]
    for _ in range(10000):
	r = c.getMove(input)
	results[r] = results[r] + 1
    for x in results: print(x/100.0) 
