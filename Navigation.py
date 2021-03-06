import battlecode as bc
import sys
import math
import Globals
import MapStrat


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
    if destination:
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
                    #print("moving along obstacle")
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


def retreatFromKnownEnemy(gc, unit, enemyLocation):
    """
    Move such that distance from known enemy increases.
    :param gc: game controller
    :param unit: unit object
    :param enemy: unit object of the enemy
    :return: True if able to move, False otherwise
    """
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
            if unitLocation.add(retreatDirection).distance_squared_to(enemyLocation) >= currentDistance:
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


def BFS(map, start, gc):
    # print("computing BFS", timeit.timeit())
    d = bc.Direction.North
    loc = start
    for i in range(8):
        if map.on_map(loc):
            if map.is_passable_terrain_at(start):
                break
        loc = start.add(d)
        d = d.rotate_right()

    if map.on_map(start):
        if map.is_passable_terrain_at(start):
            frontier = [start]
            parents = {(start.x, start.y): None}

            while frontier:
                #print(explored)
                #debug(frontier)
                frontier, parents = exploreFrontier(frontier, map, parents, gc)
            return parents
    print("somehow getting here")


def exploreFrontier(frontier, map, parent, gc):
    newFrontier = []
    d = bc.Direction.North
    for f in frontier:
        for i in range(8):
            d = d.rotate_right()
            newLocation = f.add(d)
            if map.on_map(newLocation) and (newLocation.x, newLocation.y) not in parent:
                if map.is_passable_terrain_at(newLocation):
                    if not gc.has_unit_at_location(newLocation):
                        parent[(newLocation.x, newLocation.y)] = f
                        newFrontier.append(newLocation)
    return newFrontier, parent



def reversePath(path, destination):
    end = (destination.x, destination.y)
    correctDirection = {}
    while path[end] is not None:
        correctDirection[(path[end].x, path[end].y)] = end
        end = (path[end].x, path[end].y)
    return correctDirection

#
# def debug(frontier):
#     frontier = [(frontier[i].x, frontier[i].y) for i in range(len(frontier))]
#     print(frontier)
#
#
# def allPairs(earth_map):
#     for i in range(earth_map.width):
#         for j in range(earth_map.height):
#             location = bc.MapLocation(bc.Planet.Earth, i, j)
#             x = BFS(earth_map, location)
#             Globals.paths[(i, j)] = x
#
#
# def optimalNav(gc, unit, destination):
#     ##nOT SO OPTIMAL
#     path = Globals.paths[(unit.location.map_location().x, unit.location.map_location().y)]
#     endpt = (destination.x, destination.y)
#     parent = path[endpt]
#     while parent != unit.location.map_location():
#         newSquare = parent
#         parent = path[newSquare]
#     direction = unit.location.map_location().direction_to(newSquare)
#     if gc.can_move(unit.id, direction):
#         gc.move_robot(unit.id, direction)
#     else:
#         Bug(gc, unit, destination)


def path_with_bfs(gc, unit, path):
    #also too slow
    if unit.location.is_in_garrison() or not unit.location.is_on_map():
        return False
    else:
        selfloc = unit.location.map_location()
        # planet = selfloc.planet
        # direction = selfloc.direction_to(Globals.radar.get_enemy_center(selfloc.planet))
        if unit.unit_type == bc.UnitType.Worker:
            if move_on_path(gc, unit, selfloc, path):
                return True
        if move_on_path(gc, unit, selfloc, path):
            return True
        else:
           if move_on_path(gc, unit, selfloc, Globals.pathToEnemy):
               return True
    return False

            # if not get_back_on_path(gc, unit):
            #     print("can't get on path")
            # if gc.can_move(unit.id, direction):
            #     gc.move_robot(unit.id, direction)
            # elif gc.can_move(unit.id, direction.rotate_left()):
            #     gc.move_robot(unit.id, direction.rotate_left())
            # elif gc.can_move(unit.id, direction.rotate_right()):
            #     gc.move_robot(unit.id, direction.rotate_right())


def move_on_path(gc, unit, loc, path):
    d = loc.direction_to(Globals.radar.get_enemy_center(loc.planet))
    try:
        move = path[(loc.x, loc.y)]
        if move:
            direction = loc.direction_to(move)
            if try_to_move(gc, unit, direction):
                return True
            else:
                return False

    except:
        if try_to_move(gc, unit, d):
            return True
        return False


def try_to_move(gc, unit, d):
    if gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)
        return True
    elif gc.can_move(unit.id, d):
        gc.move_robot(unit.d, d.rotate_right())
        return True
    elif gc.can_move(unit.id, d.rotate_left()):
        gc.move_robot(unit.id, d.rotate_left())
        return True
    return False


def get_back_on_path(gc, unit):
    d = bc.Direction.North
    loc = unit.location.map_location()
    planet = loc.planet
    path = Globals.pathToEnemy if planet == bc.Planet.Earth else Globals.pathToEnemyMars
    for i in range(8):
        newLoc = loc.add(d)
        if (newLoc.x, newLoc.y) in path:
            if gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                return True
    return False
#   def straightToEnemy(gc, unit):
#     start = unit.location.map_location()
#     Map = gc.starting_map(start.planet)
#     initialUnits = Map.initial_units
#     initEnemyLocations = []
#     for unit in initialUnits:
#         if unit.team != gc.team():
#             initEnemyLocations.append(unit.location.map_location())
#     paths = []
#     for loc in initEnemyLocations:
#         shortestPath = BFS(Map, start, loc)
#         paths.append(reversePath(shortestPath, loc))
#     Globals.paths_to_initial_enemylocs[unit.id] = paths
#
#
# def disperse(gc, unit):
#     start = unit.location.map_location()
#     quads = findQuadrants(gc.starting_map(start.planet))
#     paths = []
#     for loc in quads:
#         shortestPath = BFS(gc.starting_map(start.planet), start, loc)
#         paths.append(reversePath(shortestPath, loc))
#     if start.planet == bc.Planet.Earth:
#         Globals.paths_to_disperse_earth[unit.id] = paths
#     else:
#         Globals.paths_to_disperse_mars[unit.id] = paths



# def BFSKarb(map, gc):
#     carbs = Globals.radar.earth_karbonite_locations
#     for x in carbs:
#         Globals.pathsToKarb[(x.x, x.y)]= (BFS(map, x, gc))


def karbpath(gc, unit, loc):
    quad = MapStrat.get_quadrant(gc.starting_map(loc.planet), (loc.x, loc.y))
    if loc.planet == bc.Planet.Earth:
        cache = Globals.pathsToKarb
        farcache = Globals.pathsToFarKarb
        farkarb = Globals.farKarb
    else:
        cache = Globals.pathsToKarbMars
        farcache = Globals.pathsToFarKarbMars
        farkarb = Globals.farKarbMars
    if quad in Globals.pathsToKarb:
        area = cache[quad]
    else:
        if len(farcache) > 0:
            area = farcache[quad]
        else:
            Globals.pathsToFarKarb = MapStrat.doKarbBFS(farkarb, gc.starting_map(bc.Planet.Earth))
            area = Globals.pathsToFarKarb[quad]
    for path in area:
        try:
            goTo = area[path][(loc.x, loc.y)]

            if goTo:
                if gc.can_sense_location(goTo):
                    if gc.karbonite_at(goTo) > 0:
                        move = loc.direction_to(goTo)
                        if try_to_move(gc, unit, move):
                            # print("THinks its moving")
                            return True
                    else:
                        continue
        except KeyError:
            continue
    return False
    # print("END OF FUNCTION ")


def findNearestKarb(map, loc, gc):
    if map.on_map(loc):
        if map.is_passable_terrain_at(loc):
            frontier = [loc]
            parents = {(loc.x, loc.y): None}

            while frontier:
                #print(explored)
                #debug(frontier)
                frontier, parents, dest = exploreFrontierKarb(frontier, map, parents, gc)
                if dest is not None:
                    break
            if dest is not None:
                return reversePath(parents, dest), dest
            else:
                return False, dest


def exploreFrontierKarb(frontier, map, parent, gc):
    newFrontier = []
    d = bc.Direction.North
    dest = None
    for f in frontier:
        for i in range(8):
            d = d.rotate_right()
            newLocation = f.add(d)
            if map.on_map(newLocation) and (newLocation.x, newLocation.y) not in parent:
                if map.is_passable_terrain_at(newLocation):
                    # if not gc.has_unit_at_location(newLocation):
                    parent[(newLocation.x, newLocation.y)] = f
                    newFrontier.append(newLocation)
                    if (newLocation.x, newLocation.y) in Globals.radar.earth_karbonite_locations:
                        if Globals.radar.earth_karbonite_locations[(newLocation.x, newLocation.y)] != 0:
                            dest = newLocation
    return newFrontier, parent, dest


def goToKarb(map, unit, gc):
    if unit.id in Globals.pathsToKarb and Globals.pathsToKarb[unit.id] is False:
        Globals.no_karb_around[unit.id] = unit
        if len(Globals.no_karb_around) >= Globals.radar.our_num_earth_workers:
            Globals.earth_karb_gone = True
            return False
    loc = unit.location.map_location()
    if unit.id in Globals.going_to_karb:
        amount_left = Globals.radar.update_karb_amount(gc, Globals.going_to_karb[unit.id])
        if amount_left == 0:
            del Globals.pathsToKarb[unit.id]
            del Globals.going_to_karb[unit.id]
    if unit.id in Globals.pathsToKarb:
        if (loc.x, loc.y) in Globals.pathsToKarb[unit.id]:
            move = Globals.pathsToKarb[unit.id][(loc.x, loc.y)]
        else:
            Globals.pathsToKarb[unit.id], dest = findNearestKarb(map, loc, gc)
            Globals.going_to_karb[unit.id] = dest
            if unit.id in Globals.pathsToKarb and Globals.pathsToKarb[unit.id] is False:
                Globals.no_karb_around[unit.id] = unit
                if len(Globals.no_karb_around) >= Globals.radar.our_num_earth_workers:
                    Globals.earth_karb_gone = True
                    return False
            move = Globals.pathsToKarb[unit.id][(loc.x, loc.y)]
        dir = loc.direction_to(bc.MapLocation(loc.planet, move[0], move[1]))
        if gc.can_move(unit.id, dir):
            gc.move_robot(unit.id, dir)
            return True
    else:
        n, dest = findNearestKarb(map, loc, gc)
        if n:
            Globals.pathsToKarb[unit.id] = n
            Globals.going_to_karb[unit.id] = dest
            if unit.id in Globals.pathsToKarb and Globals.pathsToKarb[unit.id] is False:
                Globals.no_karb_around[unit.id] = unit
                if len(Globals.no_karb_around) >= Globals.radar.our_num_earth_workers:
                    Globals.earth_karb_gone = True
                    return False
            move = Globals.pathsToKarb[unit.id][(loc.x, loc.y)]
            dir = loc.direction_to(bc.MapLocation(loc.planet, move[0], move[1]))
            if gc.can_move(unit.id, dir):
                gc.move_robot(unit.id, dir)
                return True
        else:
            Globals.no_karb_around[unit.id] = unit
            if len(Globals.no_karb_around) >= Globals.radar.our_num_earth_workers:
                Globals.earth_karb_gone = True
                return False
    return False
