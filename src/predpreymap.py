import random
import critter
from critter import Critter

class Map:

    topleft = 1
    topright = 2
    right = 3
    bottomright = 4
    bottomleft = 5
    left = 6

    directions = []
    gooddirections = []
    critters = {}
    plants = []

    def __init__(self, size, plantpercent):

        self.size = size
        #Fill the map with plants
        for _ in range(int(plantpercent*size)):
                loc = (random.randint(0, size-1), random.randint(0, size-1))
                while loc in self.plants:
                        loc = (random.randint(0, size-1), random.randint(0, size-1))
                self.plants.append(loc)

    def isPlant(self, location):
        return location in self.plants
                
    def getCritterXY(self, critter):
        return self.critters[critter]

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

    def getTile(self, location, wheretogo):
        (x, y) = location
        if wheretogo == self.donothing:
            return (x,y)
        if wheretogo == self.topleft:
            if y == 0:
                return (-1, -1)
            if x == 0 and y%2 == 0:
                return (self.size-1, y-1)
            if y % 2 == 1:
                return (x, y-1)
            else:
                return (x-1, y-1)
        if wheretogo == self.topright:
            if y == 0:
                return (-1, -1)
            if x == self.size-1 and y%2 == 1:
                return (0,y-1)
            if y % 2 == 1:
                return (x+1, y-1)
            else:
                return (x, y-1)

        if wheretogo == self.right:
            if x == self.size - 1:
                return (0, y)
            else:
                return (x+1, y)

        if wheretogo == self.left:
            if x == 0:
                return (self.size-1, y)
            else:
                return (x-1, y)

        if wheretogo == self.bottomleft:
            if y == self.size - 1:
                return (-1, -1)
            if x == 0 and y%2 == 0:
                return (self.size-1, y+1)
            if y % 2 == 1:
                return (x, y+1)
            else:
                return (x-1, y+1)

        if wheretogo == self.bottomright:
            if y == self.size -1:
                return (-1, -1)
            if x == self.size-1 and y % 2 == 1:
                return (0, y+1)
            if y % 2 == 1:
                return (x+1, y+1)
            else:
                return (x, y+1)

    def moveCritter(self, critter, move):
        if critter not in self.critters:
            raise Exception("Critter not on map")
            return


        oldloc = self.critters[critter]
        newloc = self.getTile(oldloc, move)

        if newloc == None or newloc == (-1, -1):
            raise Exception("Can't move in that direction: ")
            return

        #made it this far, do the move
        self.removeCritter(critter)
        self.setCritterAt(newloc, critter)
            
    def removeCritter(self, critter):
        del self.critters[critter]

    def getCritters(self):
        return self.critters.keys()

    def getPreys(self):
        return filter(lambda c : c.type == "prey", self.critters)

    def getPredators(self):
        return filter(lambda c : c.type == "predator", self.critters)

    def getDirection(self,x,y,disx,disy,radius):

        test1 = -1
        test2 = -1

        # Tests To See If Organy Is Much Different Than
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
                    return self.topright

                else:
                    return self.bottomleft

            # Small Vertical Difference Organ Is Right Of Scanner
            elif test2 == 1:
                return self.right
            
            # Small Vertical Difference Organ Is Left Of Scanner
            else:
                return self.left

        # Big Vertical Difference Organ Under Scanner
        # Uses Horizontal Difference For Bottom (Right Or Left)
        # If Horizontal Even Also Bullshit Say BottomLeft
        
        elif test1 == 1:
            if test2 == 1:
                return self.bottomright
            else:
                return self.bottomleft

        # Big Vertical Difference Organ Over Scanner
        # Uses Horizontal Difference For Top (Right Or Left)
        # If Horizontal Even Also Bullshit Say TopLeft

        elif test1 == 2:
            if test2 == 1:
                return self.topright
            else:
                return self.topleft

    def getDistance(self, x, y, checkx, checky):

        # Non Scientific GetDistance
        # Uses Sqaure World Logic Not Hexagonal
        distance = abs(x-checkx) + abs(y-checky)
        return distance

    def getClosestPlant(self, x, y, radius):

        # Returns Closest Plant Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Plants
        for critter in map.plants:
            checkx = critter[0]
            checky = critter[1]
            checkdistance = self.getDistance(x,y,checkx,checky)

            # That It Is Closer Than The Previous Closest
            # That It is Closer Than Scan Radius
            if checkdistance < closest:
                    if checkdistance < radius:
                            # Changes To New Closest And Direction
                            closest = checkdistance
                            direction = self.getDirection(x,y,checkx,checky,radius)

        if direction != -1:    
                return closest, direction
        else:
                return None, None
        
    def getClosestPred(self, x, y, radius):

        # Returns Closest Pred Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Preds
        for critter in map.getPredators():
            checkx,checky = (map.getCritterXY(critter))
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
            
        if direction != -1:    
                return closest, direction
        else:
                return None, None

    def getClosestPrey(self, x, y, radius):

        # Returns Closest Prey Distance, Direction
        closest = 1000
        direction = -1

        # Goes Through All Preys
        for critter in map.getPreys():
            checkx,checky = (map.getCritterXY(critter))
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
            
        if direction != -1:    
                return closest, direction
        else:
                return None, None

    def getSensoryData(self,critter, radius):

        # Gets The X And Y Of Critter Or Plant And Checks For Closest
        # Predator, Prey or Plant
        (x,y) = self.getCritterXY(critter)
        preddistance,preddirection = self.getClosestPred(x, y, radius)
        preydistance,preydirection = self.getClosestPrey(x, y, radius)
        plantdistance,plantdirection = self.getClosestPlant(x, y, radius)

        return preddistance, preddirection, preydistance, preydirection,plantdistance,plantdirection

    def getRandomUntakenTile(self):
        if len(self.critters) >= self.size**2:
                raise Exception("No more untaken tiles exist")
        loc = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        while loc in self.critters.values():
                loc = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        return loc
        


#Only run this code if this one file is being run a python program
if __name__ == "__main__":
        import critter
        from critter import Critter

        map = Map(100, 0.5)

        pred1 = Critter(critter.PREDATOR)
        pred2 = Critter(critter.PREDATOR)
        pred3 = Critter(critter.PREDATOR)
        prey1 = Critter(critter.PREY)
        prey2 = Critter(critter.PREY)
        prey3 = Critter(critter.PREY) 

        map.setCritterAt((0,2), pred1)
        map.setCritterAt((6,8), pred2)
        map.setCritterAt((10,14), pred3)
        map.setCritterAt((3,4), prey1)
        map.setCritterAt((8,12), prey2)
        map.setCritterAt((4,5), prey3)

        print(map.getSensoryData(pred1, 20)[0] == 12)
        print(map.getSensoryData(pred1, 20)[1] == 4)
        print(map.getSensoryData(pred1, 20)[2] == 5)
        print(map.getSensoryData(pred1, 20)[3] == 3)
                                
        print(map.getSensoryData(prey2, 20)[0] == 4)
        print(map.getSensoryData(prey2, 20)[1] == 3)
        print(map.getSensoryData(prey2, 20)[2] == 11)
        print(map.getSensoryData(prey2, 20)[3] == 1)
        
        print(map.getSensoryData(pred3, 20)[0] == 10)
        print(map.getSensoryData(pred3, 20)[1] == 1)
        print(map.getSensoryData(pred3, 20)[2] == 4)
        print(map.getSensoryData(pred3, 20)[3] == 6)
        
        print(map.getSensoryData(prey3, 20)[0] == 5)
        print(map.getSensoryData(prey3, 20)[1] == 3)
        print(map.getSensoryData(prey3, 20)[2] == 2)
        print(map.getSensoryData(prey3, 20)[3] == 6)

        #print(len(map.plants) == 50) 
        #print(map.getCritterAt((3,2)) == pred)
        #print(map.getCritterAt((3,4)) == prey)
        #print(map.getCritterXY(pred) == (3, 2))
        #print(map.getCritterXY(prey) == (3, 4))
        #print(map.getCritterDest(pred, map.right) == (4, 2))
        #print(map.getTile((3,4), map.left) == (2, 4)) 
        #map.moveCritter(pred, map.right)
        #print(map.getCritterXY(pred) == map.getTile((3, 2), map.right))
        #print(map.getCritterXY(pred) == (4, 2) )
        #print(len(map.getCritters()) == 2)
        #map.removeCritter(pred)
        #print(len(map.getCritters()) == 1)
        #map.setCritterAt((5, 5), pred)
        #print(len(map.getCritters()) == 2)
        #print(map.getSensoryData(pred, 5))
        #print(map.getPreys())
        #print(map.getPredators())

