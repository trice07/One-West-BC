import battlecode as bc

import Globals
import Navigation
import Units
import time


def send_radar_info(unit, gc):
    nearby_enemies = Globals.radar.update_radar(gc, unit)
    return nearby_enemies


def turn(gc, unit):
    # t = time.time()
    result = Units.shoot_at_best_target(gc, unit)
    # Globals.ranger_find_time += time.time() - t
    # print("find target time", Globals.ranger_find_time)
    if isinstance(result, bc.Unit):
        return
    elif isinstance(result, bc.VecUnit):
        nearby_enemies = result
    else:
        nearby_enemies = send_radar_info(unit, gc)
    # t = time.time()
    if gc.is_move_ready(unit.id):
        e, should_retreat = ranger_retreat(unit, nearby_enemies)
        if should_retreat:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, Globals.radar.get_enemy_center(unit.location.map_location().planet))
            if moved:
                return
        if gc.is_attack_ready(unit.id):
            planet = unit.location.map_location().planet
            path = Globals.updatePath if planet == bc.Planet.Earth else Globals.updatePathMars
            Navigation.path_with_bfs(gc, unit, path)
    # Globals.ranger_else_time += time.time() - t
    # print("other ranger time", Globals.ranger_else_time)
    return


def ranger_retreat(unit, dangerous_enemies):
    if unit.health > (unit.max_health/10):
        return None, False
    violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
    for e in dangerous_enemies:
        if e.unit_type in violent_enemies and e.location.is_within_range(e.attack_range(), unit.location):
            return e, True
    return None, False
