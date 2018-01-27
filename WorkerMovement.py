import battlecode as bc
import sys
import time
import Globals
import Navigation


def findNearestKarb(gc, unit):
    """
    Navigate towards nearest karbonite deposit, assumes defensive path
    :param gc: game controller
    :param unit: unit object
    :return: none
    """
    nearestLoc = None
    closestKarb = sys.maxsize
    if gc.planet() == bc.Planet.Earth:
        carbs = Globals.radar.earth_karbonite_locations
    else:
        carbs = Globals.radar.mars_karbonite_locations
    s = time.time()
    for carboLoad in carbs:
        if carboLoad.distance_squared_to(unit.location.map_location()) < closestKarb:
            closestKarb = carboLoad.distance_squared_to(unit.location.map_location())
            nearestLoc = carboLoad
    Globals.ftime = (time.time()-s)
    return closestKarb, nearestLoc

