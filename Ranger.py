import battlecode as bc

import Globals
import Navigation
import Units


def send_radar_info(unit, gc):
    nearby_enemies = Globals.radar.update_radar(gc, unit)
    return nearby_enemies


def turn(gc, unit):
    result = Units.shoot_at_best_target(gc, unit)
    if isinstance(result, bc.Unit):
        return
    if gc.is_move_ready(unit.id):
        if ranger_retreat(unit):
            moved = Navigation.retreatFromKnownEnemy(gc, unit, Globals.radar.get_enemy_center(unit.location.map_location().planet))
            if moved:
                return
        planet = unit.location.map_location().planet
        path = Globals.updatePath if planet == bc.Planet.Earth else Globals.updatePathMars
        Navigation.path_with_bfs(gc, unit, path)
    return


def ranger_retreat(unit):
    return unit.health <= (unit.max_health/8)
