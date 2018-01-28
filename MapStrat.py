import battlecode as bc
import Globals
import math


def initial_distance():
    us = [Globals.radar.our_earth_locations[unit].location.map_location() for unit in Globals.radar.our_earth_locations]
    enemies = [Globals.radar.earth_enemy_locations[unit].location.map_location() for unit in Globals.radar.earth_enemy_locations]
    mindistance = 1000000000000
    for unit in range(len(us)):
        for thing in range(len(enemies)):
            dist = us[unit].distance_squared_to(enemies[thing])
            if dist < mindistance:
                mindistance = dist
    return mindistance


def initial_quadrants(map):
    us = [Globals.radar.our_earth_locations[unit].location.map_location() for unit in Globals.radar.our_earth_locations]
    quadrants = set()
    for unit in us:
        quadrants.add(get_quadrant(map, (unit.x, unit.y)))
    return quadrants


def get_quadrant(planetmap, loc):
    width = planetmap.width
    height = planetmap.height
    xhalf = math.floor(width / 2)
    yhalf = math.floor(height / 2)
    if loc[0] < xhalf:
        if loc[1] < yhalf:
            return 0
        else:
            return 1
    else:
        if loc[1] > yhalf:
            return 2
        else:
            return 3


def karbBFS(map, quadrants):
    karbDests = {}
    farKarbDests = {}
    if map.planet == bc.Planet.Earth:
        karb = Globals.radar.earth_karbonite_locations
    else:
        karb = Globals.radar.mars_karbonite_locations

    for deposit in karb:
        quad = get_quadrant(map, deposit)
        if quad in quadrants:
            if quad in karbDests:
                karbDests[quad].append(bc.MapLocation(map.planet, deposit[0], deposit[1]))
            else:
                karbDests[quad] = [bc.MapLocation(map.planet, deposit[0], deposit[1])]
        else:
            if quad in farKarbDests:
                farKarbDests[quad].append(bc.MapLocation(map.planet, deposit[0], deposit[1]))
            else:
                farKarbDests[quad] = [bc.MapLocation(map.planet, deposit[0], deposit[1])]
    if map.planet == bc.Planet.Earth:
        Globals.farKarb = farKarbDests
    else:
        Globals.farKarbMars = farKarbDests
    return doKarbBFS(karbDests, map)


def doKarbBFS(karbDests, map):
    paths = {}
    if map.planet == bc.Planet.Earth:
        cache = Globals.radar.earth_karbonite_locations
    else:
        cache = Globals.radar.mars_karbonite_locations
    for area in karbDests:
        toGet = karbDests[area]
        paths_in_quad = {}
        for i in range(len(toGet)):
            if cache[(toGet[i].x, toGet[i].y)] != 0:
                karbonite = toGet[i]
                frontier = [karbonite]
                parents = {(karbonite.x, karbonite.y): None}
                while frontier:
                    frontier, parents = exploreKarbFrontier(frontier, map, parents, area)
                paths_in_quad[(toGet[i].x, toGet[i].y)] = parents
        paths[area] = paths_in_quad
    return paths


def exploreKarbFrontier(frontier, map, parent, quadrant):
    newFrontier = []
    d = bc.Direction.North
    for f in frontier:
        for i in range(8):
            d = d.rotate_right()
            newLocation = f.add(d)
            if map.on_map(newLocation) and (newLocation.x, newLocation.y) not in parent:
                if map.is_passable_terrain_at(newLocation):
                    if get_quadrant(map, (newLocation.x, newLocation.y)) == quadrant:
                        parent[(newLocation.x, newLocation.y)] = f
                        newFrontier.append(newLocation)
                        # if (newLocation.x, newLocation.y) in Globals.radar.earth_karbonite_locations:
                        #     Globals.radar.earth_karbonite_locations[(newLocation.x, newLocation.y)] = 0
    return newFrontier, parent


def get_paths_to_karb(map):
    if map.planet == bc.Planet.Mars:
        quads = {0, 1, 2, 3}
    else:
        quads = initial_quadrants(map)
    paths = karbBFS(map, quads)
    return paths
