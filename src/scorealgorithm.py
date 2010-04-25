import random
from predpreymap import Map
from critter import Critter
import critter

try:
    import psyco
    psyco.full()
except ImportError:
    import sys
    sys.stderr.write("Install Python Psyco For Increased Performance.\nAlgo\n")

def reverse(direction):
    if direction == 0:
        return 0
    if direction <= 3:
        direction += 3
    else:
        direction -= 3
    return direction

def left(direction):
    if direction == 0:
        return 0
    if direction == 1:
        return 6
    else:
        return direction - 1

def right(direction):
    if direction == 0:
        return 0
    if direction == 6:
        return 1
    else:
        return direction + 1

#This converts for example "Move towards predator" to "Move left"
#sensorydata holds the data from the map
#move holds a direction like "Move towards predator"
def directionConverter(sensorydata):
    toPred = sensorydata[1]
    toPrey = sensorydata[3]
    toPlant = sensorydata[5]

    toPred = 0 if toPred == None else toPred
    toPrey = 0 if toPrey == None else toPrey
    toPlant = 0 if toPlant == None else toPlant
    allpossiblemoves = [toPred,  toPrey,  toPlant,
     reverse(toPred), reverse(toPrey), reverse(toPlant),
     left(toPred),    left(toPrey),    left(toPlant),
     right(toPred),   right(toPrey),   right(toPlant), 0  ]
    return allpossiblemoves

def getAMove(critter, world, settings):
        if world.getCritterXY(critter) == None:
                raise Exception("Critter isn't on the map!")
        senses = world.getSensoryData(critter, settings["sight"])
        dirconv = directionConverter(senses)
        validmoves = list(set(dirconv)) #removes all duplicates in the list
        while len(validmoves) > 0:
                destinationTile = None
                directionMove = -1
                while destinationTile == None or directionMove == -1 or directionMove == None or directionMove not in validmoves:
                        move = critter.getMove(senses)
                        directionMove = dirconv[move]
                        destinationTile = world.getCritterDest(critter, directionMove)
                if directionMove in validmoves:
                        validmoves.remove(directionMove)
                else:
                        raise Exception("%d not in %s"%(directionMove, validmoves))
                yield destinationTile, directionMove

def preyMakeMove(prey, settings, world):
        for destinationTile, directionMove in getAMove(prey, world, settings):
                critterOnTile = world.getCritterAt(destinationTile)
                if critterOnTile == None:
                        world.moveCritter(prey, directionMove)
                        if world.isPlant(destinationTile): 
                                #isPlant bites for me
                                prey.setStatus("hunger", 0)
                        return
                elif critterOnTile.type == critter.PREY:
                        continue
                elif critterOnTile.type == critter.PREDATOR:
                        world.removeCritter(prey)
                        critterOnTile.setStatus("hunger", 0)
                        return
                else:
                     raise Exception("There is a prey case that is not accounted for: " + critterOnTile)

def predMakeMove(pred, settings, world):
        for destinationTile, directionMove in getAMove(pred, world, settings):
                critterOnTile = world.getCritterAt(destinationTile)
                if critterOnTile == None:
                        world.moveCritter(pred, directionMove)
                        return
                elif critterOnTile.type == critter.PREY:
                        world.removeCritter(critterOnTile)
                        pred.setStatus("hunger", 0)
                        return
                elif critterOnTile.type == critter.PREDATOR:
                        continue                        
                else:
                     raise Exception("There is a predator case that is not accounted for: " + critterOnTile)

def calcscore(x):
    predpdf, pred_mask = x[0]
    preypdf, prey_mask = x[1]

    settings = x[2] if len(x) > 2 else DEFAULT_SETTINGS
    mapsize = settings["mapsize"] if "mapsize" in settings else 20
    vegpercent = settings["vegpercent"] if "vegpercent" in settings else 0.5
    plantbites = settings["plantbites"] if "plantbites" in settings else 3
    preypercent = settings["preypercent"] if "preypercent" in settings else 0.1
    predpercent = settings["predpercent"] if "predpercent" in settings else 0.1
    maxhunger = settings["maxhunger"] if "maxhunger" in settings else 20
    sight = settings["sight"] if "sight" in settings else 20

    hooker = x[3] if len(x) > 3 else None

    world = Map(mapsize, vegpercent,plantbites)
    for _ in range(int((mapsize**2)*predpercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(predpdf, pred_mask, critter.PREDATOR))

    for _ in range(int((mapsize**2)*preypercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(preypdf, prey_mask, critter.PREY))

    score = 0
    while len(world.getPredators()) > 0 and len(world.getPreys()) > 0:
        score += 1
        critters = world.getPredators() + world.getPreys()
        random.shuffle(critters)
        if critters == None:
                raise Exception("Critter cannot be none!!")
        for c in critters:
                if world.getCritterXY(c) == None: continue
                c.incrementStatus("hunger", 1)
                if c.type == critter.PREY:
                        preyMakeMove(c, settings, world)
                elif c.type == critter.PREDATOR:
                        predMakeMove(c, settings, world)
                else:
                        raise Exception("Something that is not a critter is in the map: " + c)
                if c.getStatus("hunger") >= settings["maxhunger"] and world.getCritterXY(c) != None:
                        world.removeCritter(c)
                if hooker != None:
                        hooker(world, score)

    if hooker != None:
        hooker(world, score)

    return score

