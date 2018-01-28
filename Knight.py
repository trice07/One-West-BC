import battlecode as bc

import Globals
import Navigation
import Units


def turn(gc, unit):
    result = Units.shoot_at_best_target(gc, unit)
    if isinstance(result, bc.Unit):
        return
    if gc.is_move_ready(unit.id):
        planet = unit.location.map_location().planet
        path = Globals.updatePath if planet == bc.Planet.Earth else Globals.updatePathMars
        Navigation.path_with_bfs(gc, unit, path)
    return


