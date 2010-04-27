import random
from predpreymap import Map
from critter import Critter
import critter
import predpreyalgorithm as ppa

def preyMakeMove(prey, world):
        for directionMove in prey.getMoves(world.getSensoryData(prey, ppa.getSetting("sight"))):
                destinationTile = world.getCritterDest(prey, directionMove)
                if destinationTile == None: continue
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

def predMakeMove(pred, world):
        for directionMove in pred.getMoves(world.getSensoryData(pred, ppa.getSetting("sight"))):
                destinationTile = world.getCritterDest(pred, directionMove)
                if destinationTile == None: continue
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

def calcscore(pred_mask, prey_mask, hooker=None):
    mapsize = ppa.getSetting("mapsize")
    vegpercent = ppa.getSetting("plantpercent")
    plantbites = ppa.getSetting("plantbites")
    preypercent = ppa.getSetting("preypercent")
    predpercent = ppa.getSetting("predpercent")
    maxhunger = ppa.getSetting("maxhunger")
    sight = ppa.getSetting("sight")

    world = Map()
    for _ in range(int((mapsize**2)*predpercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(pred_mask, critter.PREDATOR))

    for _ in range(int((mapsize**2)*preypercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(prey_mask, critter.PREY))

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
                        preyMakeMove(c, world)
                elif c.type == critter.PREDATOR:
                        predMakeMove(c, world)
                else:
                        raise Exception("Something that is not a critter is in the map: " + c)
                if c.getStatus("hunger") >= ppa.getSetting("maxhunger") and world.getCritterXY(c) != None:
                        world.removeCritter(c)
                if hooker != None:
                        hooker(world, score)

    if hooker != None:
        hooker(world, score)

    return score

