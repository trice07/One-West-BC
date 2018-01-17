import battlecode as bc
import Navigation
import sys


def findNearestKarb(gc, unit):
    """
    Navigate towards nearest karbonite deposit, assumes defensive path
    :param gc: game controller
    :param unit: unit object
    :return: none
    """
    closestKarb = sys.maxsize
    nearestLoc = None
    radarVision = gc.get_team_array(gc.planet())[0]
    carbs = radarVision.earth_karboniteLocations if gc.planet() == bc.Planet.Earth else radarVision.mars_karboniteLocations
    for carboLoad in carbs:
        if carboLoad.distance_squared_to(unit.location.map_location()) < closestKarb:
            closestKarb = carboLoad.distance_squared_to(unit.location.map_location())
            nearestLoc = carboLoad
    Navigation.Bug(gc, unit, nearestLoc, True)
