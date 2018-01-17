import battlecode as bc
import sys

def avoidEnemies(gc, unit, destination):
    """
    Navigation function for avoiding enemies, would be most useful for workers
    :param gc: game controller
    :param unit: Unit object (robot)
    :param destination: Map Location of desired destination
    :return: None
    """
    Bug(gc, unit, destination, True)
    
def Bug(gc, unit, destination, defense=False):
    """
    Movement algorithm that tries to go in the proper direction and begins circumnavigating if obstacle is present
    :param gc: game controller object
    :param unit: unit object (robot)
    :param destination: MapLocation object of desired destination
    :param defense: boolean representing if the robot should avoid enemies or not
    :return: None
    """
    location = unit.location.map_location()
    direction = location.direction_to(destination)
    if defense:
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
            gc.move_robot(unit.id, direction)
        else:
            startBugging(gc, unit, location, direction, destination, True)
    else:
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
            gc.move_robot(unit.id, direction)
        else:
            startBugging(gc, unit, location, direction, destination)

def find_closest_target(unit, enemy_map, planet):
        best=None
        target=bc.MapLocation(bc.Planet.Earth, -1, -1)
        me=unit.location.map_location()
        for enemy in enemy_map:
            them=bc.MapLocation(planet, enemy[0], enemy[1])
            distance=me.distance_squared_to(them)
            if best==None or distance<best:
                best=distance
                target=them
        return target

def isDangerousLocation(gc, unit, location):
    """
    Determines whether enemy can attack a given location
    :param gc: game controller
    :param unit: unit object
    :param location: Map Location object
    :return: None
    """
    radius = unit.vision_range
    currentLocation = unit.location.map_location()
    enemy = bc.Team.red if gc.team() == bc.Team.blue else bc.Team.blue
    enemies = gc.sense_nearby_units_by_team(currentLocation, radius, enemy)
    for evilRobot in enemies:
        if evilRobot.unit_type == bc.UnitType.Worker:
            pass
        else:
            if evilRobot.attackrange() < location.distance_squared_to(evilRobot.location.map_location()):
                return True
    return False

def random_movement(gc, unit, direction):
    """
    Moves the robot in a random direction. Takes a GameController object, a unit,
    and a direction as inputs.
    """
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
        gc.move_robot(unit.id, direction)

def retreat(gc, unit):
    """
    Run away
    :param gc: game controller
    :param unit: unit object
    :return: None
    """
    currentLocation = unit.location.map_location()
    enemy = bc.Team.red if gc.team() == bc.Team.blue else bc.Team.blue
    enemies = gc.sense_nearby_units_by_team(currentLocation, 50, enemy)
    central = findEnemyCenter(gc, enemies)
    Bug(gc, unit, central, True)

def startBugging(gc, unit, start, direction, destination, defense=False):
    """
    Function for moving around obstacle, in way such that distance to destination is still minimized
    :param gc: game controller
    :param unit: unit object (robot)
    :param start: current unit Map Location
    :param direction: optimal direction of movement to destination
    :param destination: Map Location of desired destination
    :param defense: boolean representing whether enemies should be avoided
    :return:
    """
    rightdist, leftdist = sys.maxsize, sys.maxsize
    for i in range(8):
        tryRight = direction.rotate_right()
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, tryRight):
            newLoc = start.add(tryRight)
            rightdist = newLoc.distance_squared_to(destination)
            break

    for i in range(8):
        tryLeft = direction.rotate_left()
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, tryLeft):
            newLoc = start.add(tryLeft)
            leftdist = newLoc.distance_squared_to(destination)
            break

    if rightdist < leftdist:
        wallDir = tryRight.rotate_left()
        for i in range(8):
            wallDir = wallDir.rotate_right()
            if defense:
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, wallDir):
                    gc.move_robot(unit.id, wallDir)
                    break
            else:
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, wallDir):
                    gc.move_robot(unit.id, wallDir)
                    break
    else:
        wallDir = tryLeft.rotate_right()
        for i in range(8):
            wallDir = wallDir.rotate_left()
            if defense:
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, wallDir):
                    gc.move_robot(unit.id, wallDir)
                    break
            else:
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, wallDir):
                    gc.move_robot(unit.id, wallDir)
                    break
