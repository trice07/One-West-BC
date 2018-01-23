import battlecode as bc
import sys

import Globals
import Navigation


def findNearestKarb(gc, unit):
    """
    Navigate towards nearest karbonite deposit, assumes defensive path
    :param gc: game controller
    :param unit: unit object
    :return: none
    """
    closestKarb = sys.maxsize
    nearestLoc = None
    if gc.planet() == bc.Planet.Earth:
        carbs = Globals.radar.earth_karbonite_locations
    else:
        carbs = Globals.radar.mars_karbonite_locations
    for carboLoad in carbs:
        if carboLoad.distance_squared_to(unit.location.map_location()) < closestKarb:
            closestKarb = carboLoad.distance_squared_to(unit.location.map_location())
            nearestLoc = carboLoad
    if nearestLoc is not None:
        Navigation.Bug(gc, unit, nearestLoc)
