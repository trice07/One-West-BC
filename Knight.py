import battlecode as bc

import Globals
import Navigation
import Units


def turn(gc, unit):
    Units.shoot_at_best_target(gc, unit)
    if gc.is_move_ready(unit.id):
        planet = unit.location.map_location().planet
        path = get_closest_fact(unit) if planet == bc.Planet.Earth else Globals.updatePathMars
        Navigation.path_with_bfs(gc, unit, path)
    return


def get_closest_fact(unit):
    best_d = 1000000
    best = None
    our_ml = unit.location.map_location()
    for f in Globals.pathToFactory:
        ml = bc.MapLocation(bc.Planet.Earth, f[0], f[1])
        distance = ml.distance_squared_to(our_ml)
        if distance < best_d:
            best_d = distance
            best = f
    if best is not None:
        return Globals.pathToFactory[best]
    return Globals.updatePath
