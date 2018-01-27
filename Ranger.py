import battlecode as bc

import Globals
import Navigation
import Units


def send_radar_info(unit, gc):
    nearby_enemies = Globals.radar.update_radar(gc, unit)
    return nearby_enemies


def turn(gc, unit):
    result = Units.shoot_at_best_target(gc, unit)
    if isinstance(result, bc.VecUnit):
        nearby_enemies = result
    elif result is None:
        nearby_enemies = send_radar_info(unit, gc)
    elif isinstance(result, bc.Unit):
        return
    else:
        print("What the f")
        return
    if gc.is_move_ready(unit.id):
        if Units.try_to_retreat(unit, nearby_enemies):
            moved = Navigation.retreatFromKnownEnemy(gc, unit, Globals.radar.get_enemy_center(unit.location.map_location().planet))
            if moved:
                return
        planet = unit.location.map_location().planet
        path = Globals.pathToEnemy if planet == bc.Planet.Earth else Globals.pathToEnemyMars
        Navigation.path_with_bfs(gc, unit, path)
    return
