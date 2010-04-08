#If you change this please let Sandro know
topleft = 1
topright = 2
right = 3
bottomright = 4
bottomleft = 5
left = 6

donothing = 0
max = 100
directions = []
gooddirections = []
critters = {}

# 0 For Predator
# 1 For Prey
# 2 For Plant

def getCritterAt(x,y,organ):

        # If organ is 0 look for predator
        # If organ is 1 look for prey
        # If organ is 2 look for plant
 
        # Bullshit Plese Define
        # Takes In X,Y,And Animal
        # Lets Use This Function For Testing To
        # See If Predator Or Prey Is There
        # Returns 1 If True And Zero If False
        p = 0
        if x == y:
                return 1

def setCritter(x, y, critter):
        critters[critter] = (x,y)

def removeCritter(critter):
        del critters[critter]

def getCritters():
        return critters

def countDistance(work,radius):

        # Counts Amount Of Steps In A Path
        # A Zero Is No Steps 
        count = 0;
        for x in range(0,radius):
                if work[x] != 0:
                        count = count + 1
        return count

def getDirection(x,y,disx,disy,radius):

        test1 = -1
        test2 = -1

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

        if test1 == 0:
                if test2 == 0:
                        if disy > y:
                                return topright

                        else:
                                return bottomleft

                elif test2 == 1:
                        return right
                
                else:
                        return left

        elif test1 == 1:
                if test2 == 1:
                        return bottomright
                else:
                        return bottomleft

        elif test1 == 2:
                if test2 == 1:
                        return topright
                else:
                        return topleft

def getClosestPlant(x, y, radius):

        getClosestOrganism(x, y, radius, 2)

def getClosestPred(x, y, radius):

        getClosestOrganism(x, y, radius, 0)

def getClosestPrey(x, y, radius):

        getClosestOrganism(x, y, radius, 1)

def getClosestOrganism(x,y,radius,organ):

        # Goes Through The Good Array
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
        length = checkPath(radius)
        #length = pow(7,radius)
    
        for j in range(0,(radius*length),radius):
                k = 0
                work = []
                while k < radius:
                        work.insert(k, gooddirections[j+k])
                        k = k + 1
                distance = countDistance(work,radius)

                # Uses Each Path And Does The Move To
                # Get New Tile
                # Tile Is Then Tested For Critter
                maybex = x
                maybey = y

                for p in range(0,radius):
                        maybex,maybey = getTile(maybex,maybey,work[p])

                #print(work)
                #print(x,y,maybex,maybey,distance)

                if maybex != x and maybey != y and maybex != -1 and maybex != -1: 
                        if getCritterAt(maybex,maybey,organ) == 1:
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
                direction = getDirection(x,y,disx,disy,radius)
                return closest, direction, disx, disy
        else:
                return -1, -1, -1, -1
        #print(disx,disy,closest)
        #return disx, disy, closest

def checkPath(radius):

        #Gets 1D Python Array And Puts Elements In Good Order
        length = getAllDirections(radius)
        #length = pow(7,radius)
        
        for x in range(0,length):
                for y in range(0,radius):
                    gooddirections.append(directions[(length*y) + x])
                   
        #print (gooddirections)
        return length
                    
def getAllDirections(radius):

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
                                        directions.append(x)
                                        z = z + 1
                z = 0
                
                j = j -1
                choser = pow(7,j)
                if j < 0:
                        break

        return length

def getTile(x, y, wheretogo):

        if wheretogo == donothing:
                return (x,y)
        if wheretogo == topleft:
                if y == 0:
                        return (-1, -1)
                if x == 0 and y%2 == 0:
                        return (max-1, y-1)
                if y % 2 == 1:
                        return (x, y-1)
                else:
                        return (x-1, y-1)
        if wheretogo == topright:
                if y == 0:
                        return (-1, -1)
                if x == max-1 and y%2 == 1:
                        return (0,y-1)
                if y % 2 == 1:
                        return (x+1, y-1)
                else:
                        return (x, y-1)

        if wheretogo == right:
                if x == max - 1:
                        return (0, y)
                else:
                        return (x+1, y)

        if wheretogo == left:
                if x == 0:
                        return (max-1, y)
                else:
                        return (x-1, y)

        if wheretogo == bottomleft:
                if y == max - 1:
                        return (-1, -1)
                if x == 0 and y%2 == 0:
                        return (max-1, y+1)
                if y % 2 == 1:
                        return (x, y+1)
                else:
                        return (x-1, y+1)

        if wheretogo == bottomright:
                if y == max -1:
                        return (-1, -1)
                if x == max-1 and y % 2 == 1:
                        return (0, y+1)
                if y % 2 == 1:
                        return (x+1, y+1)
                else:
                        return (x, y+1)

#Only run this code if this one file is being run a python program
if __name__ == "__main__":

    print(getClosestOrganism(6, 7, 3,0) == (2, 1, 5, 5))
    print(getClosestOrganism(32, 35, 3,0) == (2, 2, 33, 33))
    print(getClosestOrganism(32, 40, 3,0) == (-1, -1, -1, -1))


