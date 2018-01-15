import battlecode as bc
import sys

def Bug(gc, unit, destination):
    location = unit.location.map_location()
    print("Current Location: " + str(location.x) + ", " + str(location.y))
    direction = location.direction_to(destination)
    if gc.can_move(unit.id, direction):
        print("moving in direction")
        #if unit.movement_heat() < 10:
        gc.move_robot(unit.id, direction)
    else:
        startBugging(gc, unit, location, direction, destination)


def startBugging(gc, unit, start, direction, destination):
    rightdist, leftdist = sys.maxsize, sys.maxsize
    for i in range(8):
        tryRight = direction.rotate_right()
        if gc.can_move(unit.id, tryRight):
            newLoc = start.add(tryRight)
            rightdist = newLoc.distance_squared_to(destination)
            break

    for i in range(8):
        tryLeft = direction.rotate_left()
        if gc.can_move(unit.id, tryLeft):
            newLoc = start.add(tryLeft)
            leftdist = newLoc.distance_squared_to(destination)
            break

    if rightdist < leftdist:
        wallDir = tryRight.rotate_left()
        for i in range(8):
            wallDir = wallDir.rotate_right()
            if gc.can_move(unit.id, wallDir):
                print("moving along wall")
                gc.move_robot(unit.id, wallDir)
                break
    else:
        wallDir = tryLeft.rotate_right()
        for i in range(8):
            wallDir = wallDir.rotate_left()
            if gc.can_move(unit.id, wallDir):
                print("moving along wall")
                #if unit.movement_heat() < 10:
                gc.move_robot(unit.id, wallDir)
                break


