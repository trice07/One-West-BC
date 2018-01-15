import battlecode as bc
import random

def updateGarrisons(unit, garrisonDictionary, action, robotType=None):
    if action == 'build':
        if unit.id in garrisonDictionary:
            garrisonDictionary[unit.id] = garrisonDictionary.append(robotType)
        else:
            garrisonDictionary[unit.id] = [robotType]

    if action == 'unload':
        garrisonDictionary[unit.id] = []


def nextBuild(unit, queueDict):
    factoryQueue = [bc.UnitType.Knight, bc.UnitType.Knight, bc.UnitType.Knight, bc.UnitType.Mage, bc.UnitType.Healer, bc.UnitType.Worker, bc.UnitType.Worker, bc.UnitType.Worker]
    robotIndex = queueDict[unit.id]
    return factoryQueue[robotIndex]


def updateQueue(unit, queueDict):
    queueDict[unit.id] += 1


def squadUnload(gc, unit, garrisonDictionary):
    direction = random.choice(bc.Direction)
    count = 0
    for robot in garrisonDictionary[unit.id]:
        if gc.can_unload(unit.id, direction + count):
            gc.unload(unit.id, direction + count)
            count += 1


def round(gc, unit, garrisonDictionary, queueDict):
    if not unit.is_factory_producing:
        if len(garrisonDictionary[unit.id]) == 5:
            squadUnload(gc, unit, garrisonDictionary)
            updateGarrisons(unit, garrisonDictionary, 'unload')
        elif bc.UnitType.Worker in garrisonDictionary[unit.id]:
            direction = random.choice(bc.Direction)
            if gc.can_unload(unit.id, direction):
                gc.unload(unit.id, direction)
                updateGarrisons(unit, garrisonDictionary, 'unload')
        robot = nextBuild(unit, queueDict)
        if gc.can_produce_robot(unit.id, robot):
            gc.produce_robot(unit.id, robot)
            updateGarrisons(unit, garrisonDictionary, 'build', robot)
