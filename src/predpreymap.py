import random
import critter
#from critter import Critter
import predpreyalgorithm as ppa

#HardCoded Move Values
#Done For Coder Easyness
#In A Circle
dontmove = 0
topleft = 1
topright = 2
right = 3
bottomright = 4
bottomleft = 5
left = 6

class Map:

    def __init__(self):
        
        self.directions = []
        self.gooddirections = []
        self.critters = {}
        self.plants = []

        #Gets Mapsize, PlantBites and PlantPercent Setting From Algorithm
        self.size = ppa.getSetting("mapsize")
        self.plantbites = ppa.getSetting("plantbites")
        self.plantpercent = ppa.getSetting("plantpercent")
        
        #Fill The Map With Plants Using Percentage
        for _ in range(int(self.plantpercent*self.size*self.size)):
                #Puts Plant In Random Location
                loc = (random.randint(0, self.size-1), random.randint(0, self.size-1),self.plantbites)
                while loc in self.plants:
                        loc = (random.randint(0, self.size-1), random.randint(0, self.size-1),self.plantbites)
                self.plants.append(loc)

    def isPlant(self, location):

        x,y = location
        # Goes Through Plants To See If Plant There
        # If So Plant Eaten And Returned True
        for i in range (len(self.plants)):
            j,k,l = self.plants[i]
            if x == j and y == k:
                #If True Then Plant Is Eaten
                #If Plant Life Is 1 Then 1-1=0 And Plant Is BushedBombed
                if l == 1:
                    self.bushbombplants(i)
                else:
                    #Plant Life > 1 and Its Life Decreased By One
                    self.plants[i] = j,k,l-1
                return True
        #No Plant At Location
        return False

    def getCritterXY(self, critter):
        if critter in self.critters:
            return self.critters[critter]
        else:
            return None

    def getCritterAt(self,location):
        for critter in self.critters:
            if location == self.critters[critter]:
                return critter
        return None

    def setCritterAt(self, location, critter):
        self.critters[critter] = location

    def getCritterDest(self, critter, move):
        if critter not in self.critters:
                    raise "This critter was never added to the map"
        return self.getTile( self.critters[critter], move)

    #Uses Hexagonal World Logic To Get Next Title Using A Direction
    #And Current Title, Uses Cyclinder World Logic
    def getTile(self, location, wheretogo):
        (x, y) = location
        if wheretogo == -1:
            return None
        if wheretogo == 0:
            return location
        if wheretogo == topleft:
            if y == 0:
                return None
            if x == 0 and y%2 == 0:
                return (self.size-1, y-1)
            if y % 2 == 1:
                return (x, y-1)
            else:
                return (x-1, y-1)
        if wheretogo == topright:
            if y == 0:
                return None
            if x == self.size-1 and y%2 == 1:
                return (0,y-1)
            if y % 2 == 1:
                return (x+1, y-1)
            else:
                return (x, y-1)

        if wheretogo == right:
            if x == self.size - 1:
                return (0, y)
            else:
                return (x+1, y)

        if wheretogo == left:
            if x == 0:
                return (self.size-1, y)
            else:
                return (x-1, y)

        if wheretogo == bottomleft:
            if y == self.size - 1:
                return None
            if x == 0 and y%2 == 0:
                return (self.size-1, y+1)
            if y % 2 == 1:
                return (x, y+1)
            else:
                return (x-1, y+1)

        if wheretogo == bottomright:
            if y == self.size -1:
                return None
            if x == self.size-1 and y % 2 == 1:
                return (0, y+1)
            if y % 2 == 1:
                return (x+1, y+1)
            else:
                return (x, y+1)

    def moveCritter(self, critter, move):
        if critter not in self.critters:
            raise Exception("Critter not on map")

        newloc = self.getCritterDest(critter, move)
        if newloc == None or newloc == (-1, -1):
            raise Exception("Can't move in that direction: %d"%move)

        self.removeCritter(critter)
        self.setCritterAt(newloc, critter)

    #Gets Rid Of Plant On That Spot
    def bushbombplants(self, spot):
        del self.plants[spot]

    #Gets Rid Of Critter At That Spot
    def removeCritter(self, critter):
        del self.critters[critter]

    def getCritters(self):
        return self.critters.keys()

    #Goes Through Critters And Returns Only The Preys
    def getPreys(self):
        return [p for p in filter(lambda c : c.type == "prey", self.critters)]

    #Goes Through Critters And Returns Only The Preds
    def getPredators(self):
        return [p for p in filter(lambda c : c.type == "predator", self.critters)]

    #Uses New X,Y And Compares It To Old X,Y To Get The Direction From The Old To The New
    def getDirection(self,x,y,disx,disy,radius):

        test1 = -1
        test2 = -1

        # Predator Or Prey On A Plant
        #No Direction Needed
        if disx == x and disy == y:
                return 0

        # Tests To See If Organism Is Much Different Than
        # Self Y, If Not That Much, Basically Only
        # Left And Right
        # Test1 Is Y Difference
        # Test2 Is X Difference
        
        if abs(disy-y) < (radius / 5):
            test1 = 0

        elif disy > y:
            test1 = 1

        elif disy < y:
            test1 = 2

        # Tests Old And NewX
        #If Old Left Of New, Then New Right Of Left Else
        #Vis Vera
        if disx > x:
            test2 = 1

        elif disx < x:
            test2 = 2

        else:
            test2 = 0

        # No Switch ... Ufa
        # If Both 0 Then Only Small Y Apart
        # I Bullshit Say Right Ness If Higher And LeftNess If Lower
        # No Top And Bottom Exist
        
        if test1 == 0:
            if test2 == 0:
                if disy > y:
                    return topright

                else:
                    return bottomleft

            # Small Vertical Difference Organ Is Right Of Scanner
            elif test2 == 1:
                return right
            
            # Small Vertical Difference Organ Is Left Of Scanner
            else:
                return left

        # Big Vertical Difference Organ Under Scanner
        # Uses Horizontal Difference For Bottom (Right Or Left)
        # If Horizontal Even Also Bullshit Say BottomLeft
        
        elif test1 == 1:
            if test2 == 1:
                return bottomright
            else:
                return bottomleft

        # Big Vertical Difference Organ Over Scanner
        # Uses Horizontal Difference For Top (Right Or Left)
        # If Horizontal Even Also Bullshit Say TopLeft

        elif test1 == 2:
            if test2 == 1:
                return topright
            else:
                return topleft

    def getDistance(self, x, y, checkx, checky):

        # Non Scientific GetDistance
        # Uses Sqaure World Logic Not Hexagonal
        # Uses Z^2 = X^2 + Y^2
        xsq = abs(x-checkx)
        ysq = abs(y-checky)
        xsq = xsq * xsq
        ysq = ysq * ysq
        sq = xsq + ysq
        distance = pow(sq,.5)

        #Round Answer, And Int-ify
        return int(round(distance))

    def getClosestPlant(self, x, y, radius):

        # Returns Closest Plant Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Plants
        for critter in self.plants:
            checkx = critter[0]
            checky = critter[1]
            
            #Gets Distance To Plant
            checkdistance = self.getDistance(x,y,checkx,checky)

            # If It Is Closer Than The Previous Closest
            # If It is Closer Than Scan Radius
            if checkdistance < closest:
                    if checkdistance < radius:
                            # Changes To New Closest And Direction
                            closest = checkdistance
                            direction = self.getDirection(x,y,checkx,checky,radius)

        #If No New Direction Nothing There Return 0
        #Else Return The Closest And Direction
        if direction != -1:    
                return closest, direction
        else:
                return 0, 0
        
    def getClosestPred(self, x, y, radius):

        # Returns Closest Pred Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Preds
        for critter in self.getPredators():
            checkx,checky = (self.getCritterXY(critter))
            #Gets Distance To Critter
            checkdistance = self.getDistance(x,y,checkx,checky)

            # Sees If Pred Distance Is Not 0
            # That It Is Closer Than The Previous Closest
            # That It is Closer Than Scan Radius
            if checkdistance != 0:
                    if checkdistance < closest:
                            if checkdistance < radius:
                                    # Changes To New Closest And Direction
                                    closest = checkdistance
                                    direction = self.getDirection(x,y,checkx,checky,radius)

        #If No New Direction Nothing There Return 0
        #Else Return The Closest And Direction 
        if direction != -1:    
                return closest, direction
        else:
                return 0, 0

    def getClosestPrey(self, x, y, radius):

        # Returns Closest Prey Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Preys
        for critter in self.getPreys():
            checkx,checky = (self.getCritterXY(critter))
            #Gets Distance To Critter
            checkdistance = self.getDistance(x,y,checkx,checky)
            
            # Sees If Prey Distance Is Not 0
            # That It Is Closer Than The Previous Closest
            # That It is Closer Than Scan Radius
            if checkdistance != 0:
                    if checkdistance < closest:
                            if checkdistance < radius:
                                    # Changes To New Closest And Direction
                                    closest = checkdistance
                                    direction = self.getDirection(x,y,checkx,checky,radius)

        #If No New Direction Nothing There Return 0
        #Else Return The Closest And Direction 
        if direction != -1:
                return closest, direction
        else:
                return 0, 0

    def getChunk(self, number):
        chunks  = ppa.getSetting("distancechunks")
        for i,val in enumerate(chunks):
            if number < val:
                return i
        return len(chunks)

    #Gets The X And Y Of Critter Or Plant And Checks For Closest
    #Predator, Prey or Plant
    def getSensoryData(self, crit, radius):
        (x,y) = self.getCritterXY(crit)
        preddistance,preddirection = self.getClosestPred(x, y, radius)
        preydistance,preydirection = self.getClosestPrey(x, y, radius)
        plantdistance,plantdirection = self.getClosestPlant(x, y, radius)
        return self.getChunk(preddistance), preddirection, self.getChunk(preydistance), preydirection, self.getChunk(plantdistance),plantdirection

    def getRandomUntakenTile(self):
        if len(self.critters) >= self.size**2:
                raise Exception("No more untaken tiles exist")
        loc = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        while loc in self.critters.values():
                loc = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        return loc
        
    def __str__(self):
        s =  "Map<Prey at: " 
        s += ",".join(map((lambda p : str(self.getCritterXY(p))), self.getPreys() ) )
        s += " Preds at: " 
        s += ",".join(map((lambda p : str(self.getCritterXY(p))), self.getPredators() ) )
        s += "Plants at: " + ",".join(str(self.plants))
        s += ">"
        return s


#Only run this code if this one file is being run a python program
if __name__ == "__main__":
        map1 = Map()

        pred1 = critter.Critter(critter.PREDATOR)
        pred2 = critter.Critter(critter.PREDATOR)
        pred3 = critter.Critter(critter.PREDATOR)
        prey1 = critter.Critter(critter.PREY)
        prey2 = critter.Critter(critter.PREY)
        prey3 = critter.Critter(critter.PREY) 

        map1.setCritterAt((0,2), pred1)
        map1.setCritterAt((6,8), pred2)
        map1.setCritterAt((10,14), pred3)
        map1.setCritterAt((3,4), prey1)
        map1.setCritterAt((8,12), prey2)
        map1.setCritterAt((4,5), prey3)

        #print(map1)

        #print(map1.plants)
        location = (50,40)
        #print(map1.isPlant((location)))
        #print(map1.plants)

        print(map1.getSensoryData(pred1, 2)[0])
        print(map1.getSensoryData(pred1, 2)[1])
        print(map1.getSensoryData(pred1, 2)[2])
        print(map1.getSensoryData(pred1, 2)[3])

        print(map1.getSensoryData(pred1, 20)[0])
        print(map1.getSensoryData(pred1, 20)[1])
        print(map1.getSensoryData(pred1, 20)[2])
        print(map1.getSensoryData(pred1, 20)[3])

        print(map1.getSensoryData(prey2, 20)[0])
        print(map1.getSensoryData(prey2, 20)[1])
        print(map1.getSensoryData(prey2, 20)[2])
        print(map1.getSensoryData(prey2, 20)[3])

        print(map1.getSensoryData(pred3, 20)[0])
        print(map1.getSensoryData(pred3, 20)[1])
        print(map1.getSensoryData(pred3, 20)[2])
        print(map1.getSensoryData(pred3, 20)[3])
        print(map1.getSensoryData(prey3, 20)[0])
        print(map1.getSensoryData(prey3, 20)[1])
        print(map1.getSensoryData(prey3, 20)[2])
        print(map1.getSensoryData(prey3, 20)[3])
