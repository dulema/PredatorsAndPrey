topleft = 1
topright = 2
right = 3
left = 4
bottomleft = 5
bottomright = 6
donothing = 0
max = 4

def getCritterAt(x,y):

        p = 0

def getClosestPred(x,y):

        checkers = getTilesInRadius(x,y)
        closest = 1000
        checkx = -1
        checky = -1

        for j in range(0,checkers.length):
                if count % 3 != 0:
                        continue
                if getCritterAt(checkers[j],checkers[j+1]) == 'D':
                       if checkers[j+2] < closest:
                               closest = checkers[j+2]
                               checkx = checkers[j]
                               checky = checkers[j+1]

        return (checkx,checky,closest)

def checkPath(x,y,q,w,e,r,t):

        currentx = x
        currenty = y
        zerocount = [q,w,e,r,t]
        count = 0
        for f in range(0,6):
             if zerocount[f] != 0:
                     count = count + 1
        
        currentx,currenty = getTile(currentx,currenty,q)
        currentx,currenty = getTile(currentx,currenty,w)
        currentx,currenty = getTile(currentx,currenty,e)
        currentx,currenty = getTile(currentx,currenty,r)
        currentx,currenty = getTile(currentx,currenty,t)
        
        return (currentx,currenty,count)

def getTilesInRadius(x,y):

        # Radius Of 5 Desired, Goes Through All Possible 5 Moves
        # Does Them And If The Tile Is Not In The List Adds It
        # I Want To Say Zero Checked First
        goodscan = []
        flag = -1
        distance = -1
        for q in range(0,7):
                for w in range(0,7):
                        for e in range(0,7):
                                for r in range(0,7):
                                        for t in range(0,7):
                                                checkx,checky,distance = checkPath(x,y,q,w,e,r,t)
                                                flag = -1
                                                distance = -1
                                                for count in range(0,goodmove.length):
                                                        if count % 3 != 0:
                                                                continue
                                                        if goodmove[count] == checkx and goodmove[count+1] == checky:
                                                             flag = 1
                                                if flag == -1:
                                                        goodmove.add(checkx)
                                                        goodmove.add(checky)
                                                        goodmove.add(distance)

        return goodscan
                                                                   
#Gay, Not Right SqaureScan
def gaygetClosestPred(preyx, preyy, radius):
        horscan1 = preyx - radius
        horscan2 = preyx + radius
        verscan1 = preyy - radius
        verscan2 = preyy + radius
        closest = 50        
        closex = -1
        closey = -1
        for i in range (horscan1, horscan2):

                if i < 0:
                        checkx = mapsize + i
                if i > (mapsize-1):
                        checkx = i - mapsize 
                
                for j in range (verscan1, verscan2):

                        if j < 0 or j > (mapsize-1):
                                continue

                        checky = j
                        
                        if getCritterAt(checkx,checky) == 'D':
                                if (abs(checkx-preyx) + abs(checky-preyy)) < closest:
                                        closest = (abs(checkx-preyx) + abs(checky-preyy))
                                        closex = checkx
                                        closey = checky

        if closex != -1:
                return (closex,closey)
        else:
                return (-1,-1)


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


