#If you change this please let Sandro know

class Map:
        
        topleft = 1
        topright = 2
        right = 3
        bottomright = 4
        bottomleft = 5
        left = 6

        donothing = 0
        size = 100
        directions = []
        gooddirections = []
        critters = {}
        worldmap = {}

        # 0 For Predator
        # 1 For Prey
        # 2 For Plant

        def __init__(self, size):
                
                #Should be in the INIT when made a Class
                self.size = size
                for i in range(size):
                        for j in range(size):
                                self.worldmap[(j,i)] = ' '
                                
        def getCritterXY(self, critter):
                return self.critters[critter]

        def getCritterAt(self,x,y,organ):

                # If organ is 0 look for predator
                # If organ is 1 look for prey
                # If organ is 2 look for plant
                # Returns 1 If True And Zero If False
                
                # Bullshit Plese Define
                # Takes In X,Y,And Animal
                # Anthony Used Function For Testing To
                # See If Predator Or Prey Is There
                # Returns 1 If True And Zero If False
                
                if organ == 0:
                        #if self.worldmap[(x,y)] == "predator":
                        return 1
                        #else:
                                #return 0
                
                elif organ == 1:
                        #if self.worldmap[(x,y)] == "prey":
                        return 1
                        #else:
                                #return 0
                
                elif organ == 2:
                        #if self.worldmap[(x,y)] == "plant":
                        return 1
                        #else:
                                #return 0

        def setCritter(self, x, y, critter):
                self.critters[critter] = (x,y)
                self.worldmap[(x,y)] = critter

        def moveCritter(self, critter, move):
                if (critter in self.critters) == True:
                        #Gets Old Critter Location and deletes it from
                        #World Map
                        (oldx, oldy) = self.critters[critter]
                        self.worldmap[(oldx, oldy)] = ' '

                        #Gets New X,Y updates critter location
                        #Updates World Map
                        (x,y) = getTile((oldx, oldy), move)
                        self.critters[critter] = (x,y)
                        self.worldmap[(x,y)] = critter
                else:
                        #Should Throw exception
                        #Trying to move critter that doesn't exist
                        print ("false")
                        
        def removeCritter(self, critter):
                (x,y) = self.critters[critter]
                del self.critters[critter]
                self.worldmap[(x,y)] = ' '

        def getCritters(self):
                return critters.keys()

        def countDistance(self,work,radius):

                # Counts Amount Of Steps In A Path
                # A Zero Is No Steps
                # Work Is A List Of Directional Steps
                # Radius Is Max Amount Of Steps
                
                count = 0
                for x in range(0,radius):
                        if work[x] != 0:
                                count = count + 1
                return count

        def getDirection(self,x,y,disx,disy,radius):

                test1 = -1
                test2 = -1

                # Tests To See If Organy Is Much Different Than
                # Self Y, If Not That Much, Basically Only
                # Left And Right
                # Test1 Is Y Difference
                # Test2 Is X Difference
                
                if abs(disy-y) < (radius / 3):
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
                # Choosing Scanner Direction To Organ

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

        def getClosestPlant(self, x, y, radius):

                # Returns Closest Plant Distance, Direction, LocationX, LocationY
                plantdistance,plantdirection,plantx,planty = self.getClosestOrganism(x, y, radius, 2)
                return plantdistance,plantdirection,plantx,planty

        def getClosestPred(self, x, y, radius):

                # Returns Closest Pred Distance, Direction, LocationX, LocationY
                preddistance,preddirection,predx,predy = self.getClosestOrganism(x, y, radius, 0)
                return preddistance,preddirection,predx,predy

        def getClosestPrey(self, x, y, radius):

                # Returns Closest Prey Distance, Direction, LocationX, LocationY
                preydistance,preydirection,preyx,preyy = self.getClosestOrganism(x, y, radius, 1)
                return preydistance,preydirection,preyx,preyy

        def getClosestOrganism(self, x, y, radius, organ):

                # Goes Through The Good Array (One That Stores All Possible Paths)
                # And Pulls Out Paths One At A Time
                # Each Path Is Tested To See If There Is A Critter
                # At That Tile After The Path Is Taken
                # If There Is A Critter If It Is Closest
                # OverWrites Previous Closest
                
                closex = -1
                closey = -1
                maybex = -1
                maybey = -1
                disx = -1
                disy = -1
                direction = -1
                closest = 1000
                distance = 1000
                length = self.checkPath(radius)
                #length = pow(7,radius)
            
                for j in range(0,(radius*length),radius):
                        k = 0
                        work = []
                        while k < radius:
                                work.insert(k, self.gooddirections[j+k])
                                k = k + 1
                        distance = self.countDistance(work,radius)

                        # Uses Each Path And Does The Move To
                        # Get New Tile
                        # Tile Is Then Tested For Critter
                        # If Title Has Critter And Is Closer Than Stored, Change Stored
                        maybex = x
                        maybey = y

                        for p in range(0,radius):
                                maybex,maybey = self.getTile(maybex,maybey,work[p])

                        #print(work)
                        #print(x,y,maybex,maybey,distance)

                        if maybex != x and maybey != y and maybex != -1 and maybex != -1: 
                                if self.getCritterAt(maybex,maybey,organ) == 1:
                                     closex = maybex
                                     closey = maybey

                        else:
                                closex = -1
                                closey = -1
          
                        if closex != -1:
                                if distance < closest:
                                        #print(work)
                                        #print(x,y,maybex,maybey,distance)
                                        closest = distance
                                        disx = closex
                                        disy = closey

                        del work

                if disx != -1 and disy != -1 and closest != 1000:
                        direction = self.getDirection(x,y,disx,disy,radius)
                        #print(closest, direction, disx, disy)
                        return closest, direction, disx, disy
                else:
                        #print(closest, direction, disx, disy)
                        return -1, -1, -1, -1

        def checkPath(self,radius):

                #Gets 1D Python Array And Puts Elements In Good Order
                length = self.getAllDirections(radius)
                #length = pow(7,radius)
                
                for x in range(0,length):
                        for y in range(0,radius):
                            self.gooddirections.append(self.directions[(length*y) + x])
                           
                #print (gooddirections)
                return length
                            
        def getAllDirections(self,radius):

                # Uses Super DiFiore Logic To Dynamically
                # Generate All Steps One Can Take From A
                # Spot Using A Given Amount Of Steps
                # Loades C++ 2D Array Into Python 1D Array Called Direction
                
                j = radius - 1
                choser = pow(7,j)
                length = pow(7,radius)
                z = 0
         
                while 1:
                        while z < length: 
                                for x in range(0,7):
                                        for y in range(0,choser):
                                                self.directions.append(x)
                                                z = z + 1
                        z = 0
                        
                        j = j -1
                        choser = pow(7,j)
                        if j < 0:
                                break

                return length

        def getTile(self, x, y, wheretogo):

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

        def getSensoryData(self,critter, radius):

                (x,y) = self.getCritterXY(critter)
                preddistance,preddirection,predplacex,predplacey = self.getClosestPred(x, y, radius)
                preydistance,preydirection,preyplacex,preyplacey = self.getClosestPrey(x, y, radius)
                plantdistance,plantdirection,plantplacex,plantplacey = self.getClosestPlant(x, y, radius)

                return preddistance, preddirection, preydistance, preydirection, plantdistance, plantdirection
                
#Only run this code if this one file is being run a python program
if __name__ == "__main__":

    map1 = Map(100)
    print(map1.getClosestOrganism(6, 7, 3,0) == (2, 1, 5, 5))
    print(map1.getClosestOrganism(32, 35, 3,0) == (2, 2, 33, 33))
    print(map1.getClosestOrganism(32, 40, 3,0) == (-1, -1, -1, -1))
    print(map1.getClosestOrganism(38, 52, 5,0) == (-1, -1, -1, -1))
    print(map1.getClosestOrganism(41, 49, 5,0) == (4, 2, 44, 44))
    print(map1.getSensoryData(0,5) == (4, 2, 4, 2, 4, 2))
