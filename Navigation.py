import battlecode as bc
import sys

import Globals


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
    # print("Current Location: " + str(location.x) + ", " + str(location.y))
    direction = location.direction_to(destination)
    if defense:
        if gc.can_move(unit.id, direction) and not isDangerousLocation(gc, unit, location.add(direction)):
            # print("moving in direction")
            #if unit.movement_heat() < 10:
            gc.move_robot(unit.id, direction)
        else:
            startBugging(gc, unit, location, direction, destination, True)
    else:
        if gc.can_move(unit.id, direction):
            # print("moving in direction")
            #if unit.movement_heat() < 10:
            gc.move_robot(unit.id, direction)
        else:
            startBugging(gc, unit, location, direction, destination)


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
            if defense:
                if gc.can_move(unit.id, wallDir) and not isDangerousLocation(gc, unit, start.add(wallDir)):
                    # print("moving along obstacle")
                    gc.move_robot(unit.id, wallDir)
                    break
            else:
                if gc.can_move(unit.id, wallDir):
                    print("moving along obstacle")
                    #if unit.movement_heat() < 10:
                    gc.move_robot(unit.id, wallDir)
                    break
    else:
        wallDir = tryLeft.rotate_right()
        for i in range(8):
            wallDir = wallDir.rotate_left()
            if defense:
                if gc.can_move(unit.id, wallDir) and not isDangerousLocation(gc, unit, start.add(wallDir)):
                    # print("moving along obstacle")
                    gc.move_robot(unit.id, wallDir)
                    break
            else:
                if gc.can_move(unit.id, wallDir):
                    # print("moving along obstacle")
                    #if unit.movement_heat() < 10:
                    gc.move_robot(unit.id, wallDir)
                    break


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
    enemy = bc.Team.Red if gc.team() == bc.Team.Blue else bc.Team.Blue
    enemies = gc.sense_nearby_units_by_team(currentLocation, radius, enemy)
    for evilRobot in enemies:
        if evilRobot.unit_type == bc.UnitType.Worker or evilRobot.unit_type == bc.UnitType.Factory:
            pass
        else:
            if evilRobot.attack_range() < location.distance_squared_to(evilRobot.location.map_location()):
                return True

    return False


def avoidEnemies(gc, unit, destination):
    """
    Navigation function for avoiding enemies, would be most useful for workers
    :param gc: game controller
    :param unit: Unit object (robot)
    :param destination: Map Location of desired destination
    :return: None
    """
    Bug(gc, unit, destination, True)


def retreatFromKnownEnemy(gc, unit, enemy):
    """
    Move such that distance from known enemy increases.
    :param gc: game controller
    :param unit: unit object
    :param enemy: unit object of the enemy
    :return: True if able to move, False otherwise
    """
    enemyLocation = enemy.location.map_location()
    unitLocation = unit.location.map_location()
    direction = unitLocation.direction_to(enemyLocation)
    retreatDirection = direction.opposite()
    if gc.can_move(unit.id, retreatDirection):
        gc.move_robot(unit.id, retreatDirection)
        return True

    else:
        currentDistance = unitLocation.distance_squared_to(enemyLocation)
        for i in range(8):
            retreatDirection = retreatDirection.rotate_right()
            if unitLocation.add(retreatDirection).distance_squared_to(enemyLocation) > currentDistance:
                if gc.can_move(unit.id, retreatDirection):
                    gc.move_robot(unit.id, retreatDirection)
                    return True
        return False


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
    reflection = reflectPoint(central)
    Bug(gc, unit, reflection, True)


def findEnemyCenter(gc, enemies):
    """
    Find the center of list of enemies, as represented by the average point
    :param gc: game controller
    :param enemies: UnitVec of enemies
    :return: center Map Location
    """
    xlocs = []
    ylocs = []
    for satan in enemies:
        if satan.unit_type == bc.UnitType.Worker:
            pass
        else:
            xlocs.append(satan.location.map_location().x)
            ylocs.append(satan.location.map_location().y)
    center = bc.MapLocation(gc.planet(), int(sum(xlocs)/len(xlocs)), int(sum(ylocs)/ len(ylocs)))
    return center


def reflectPoint(location):
    x = location.x
    y = location.y
    d = (x + y)/ 2
    new_x = int(2*d - x)
    new_y = int(2*d - y)
    newPt = bc.MapLocation(location.planet, new_x, new_y)
    return newPt


def BFS(earth_map, start_location, end_location):
    s = start_location
    frontier = [s]
    parents = {(s.x, s.y): None}

    while frontier:
        #print(explored)
        #debug(frontier)
        frontier = exploreFrontier(frontier, earth_map, parents)
        if (end_location.x, end_location.y) in parents:
            return parents
    return parents


def exploreFrontier(frontier, earth_map, parent):
    newFrontier = []
    d = bc.Direction.North
    for f in frontier:
        for i in range(8):
            d = d.rotate_right()
            newLocation = f.add(d)
            if earth_map.on_map(newLocation) and (newLocation.x, newLocation.y) not in parent:
                parent[(newLocation.x, newLocation.y)] = f
                newFrontier.append(newLocation)
    return newFrontier



def debug(frontier):
    frontier = [(frontier[i].x, frontier[i].y) for i in range(len(frontier))]
    print(frontier)

def allPairs(earth_map):
    for i in range(earth_map.width):
        for j in range(earth_map.height):
            location = bc.MapLocation(bc.Planet.Earth, i, j)
            x = BFS(earth_map, location)
            Globals.paths[(i, j)] = x


def optimalNav(gc, unit, destination):
    ##nOT SO OPTIMAL
    path = Globals.paths[(unit.location.map_location().x, unit.location.map_location().y)]
    endpt = (destination.x, destination.y)
    parent = path[endpt]
    while parent != unit.location.map_location():
        newSquare = parent
        parent = path[newSquare]
    direction = unit.location.map_location().direction_to(newSquare)
    if gc.can_move(unit.id, direction):
        gc.move_robot(unit.id, direction)
    else:
        Bug(gc, unit, destination)


# def straightToEnemy(gc, factory):
#     start = factory.location.map_location()


def path_with_bfs(gc, unit, start, destination):
    earthmap = gc.starting_map(bc.Planet.Earth)
    d = bc.Direction.North
    while not earthmap.is_passable_terrain_at(destination):
        d = d.rotate_right()
        destination = destination.add(d)
    path = BFS(earthmap, start, destination)
    endpt = (destination.x, destination.y)
    parent = (path[endpt].x, path[endpt].y)
    while parent != (start.x, start.y):
        endpt = parent
        parent = (path[endpt].x, path[endpt].y)
    goTo = bc.MapLocation(bc.Planet.Earth, endpt[0], endpt[1])
    direction = unit.location.map_location().direction_to(goTo)
    if gc.can_move(unit.id, direction):
        gc.move_robot(unit.id, direction)
    else:
        Bug(gc, unit, destination)




