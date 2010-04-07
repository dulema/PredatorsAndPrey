topleft = 1
topright = 2
right = 3
left = 4
bottomleft = 5
bottomright = 6
donothing = 0
max = 4
directions = []
gooddirections = []

# 0 For Predator
# 1 For Prey

def getCritter(x,y,animal):

        p = 0

def countDistance(work,radius):

        count = 0;
        for x in range(0,radius):
                if work[x] != 0:
                        count = count + 1
        return count

def doWork(work,radius,animal,x,y):

        checkx = x
        checky = y
        print("Ufa")
        print(work[0])
        for x in range(0,radius):
                checkx,checky = getTile(checkx,checky,work[x])
                
        if checkx != x and checky != y: 
                if getCritter(checkx,checky,animal) == 1:
                        return (checkx,checky)

        else:
                return (-1,-1)
                

def getClosestAnimal(x,y,radius,animal):

        closex = -1
        closey = -1
        maybex = -1
        maybey = -1
        closest = 1000
        distance = 1000
        length = checkPath(radius)
        #length = pow(7,radius)
        print (length)
        for j in range(0,(radius*length),radius):
                k = 0
                work = []
                while k < radius:
                        work.insert(k, gooddirections[j+k])
                        k = k + 1
                distance = countDistance(work,radius)
                maybex,maybey = doWork(work,radius,animal,x,y)
                if maybex != -1 and maybey != -1:
                        if distance < closest:
                                closest = distance
                                closex = maybex
                                closey = maybey
                print(work)
                print(" ")
                print(distance)
                print("\n")
                del work

def checkPath(radius):

        length = getAllDirections(radius)
        #length = pow(7,radius)
        
        for x in range(0,length):
                for y in range(0,radius):
                    gooddirections.append(directions[(length*y) + x])
                   
        #print (gooddirections)
        return length
                    
def getAllDirections(radius):

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
    print(getTile(3, 4, donothing) == (3, 4))
    print(getTile(1, 1, topleft) == (1,0))
    print(getTile(1, 2, topright) == (1,1))
    print(getTile(1, 2, right) == (2,2))
    print(getTile(1, 2, left) == (0,2))
    print(getTile(1, 2, bottomleft) == (0,3))
    print(getTile(1, 2, bottomright) == (1,3))
    print(getTile(0, 0, topleft) == (-1, -1))
    print(getTile(0, 0, topright) == (-1, -1))
    print(getTile(2, 0, topright) == (-1, -1))
    print(getTile(2, 0, topleft) == (-1, -1))
    print(getTile(3, 3, bottomleft) == (-1, -1))
    print(getTile(3, 3, bottomright) == (-1, -1))
    print(getTile(3, 3, topright) == (0, 2))
    print(getTile(0, 2, topleft) == (3, 1))
    print(getTile(0, 0, bottomleft) == (3, 1))
    print(getTile(3, 1, bottomright) == (0, 2))
    getClosestAnimal(6,7,3,0)
   


