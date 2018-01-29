import battlecode as bc
import random
import Globals
import Navigation
import Units

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective


def send_radar_info(unit, gc):
    nearby_enemies = Globals.radar.update_radar(gc, unit)
    return nearby_enemies


def manage_mages(gc, unit):
    result = Units.shoot_at_best_target(gc, unit)
    if isinstance(result, bc.Unit):
        return
    elif isinstance(result, bc.VecUnit):
        nearby_enemies = result
    else:
        nearby_enemies = send_radar_info(unit, gc)
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
    return


def ranger_retreat(unit, dangerous_enemies):
    if unit.health > (unit.max_health/10):
        return None, False
    violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
    for e in dangerous_enemies:
        if e.unit_type in violent_enemies and e.location.is_within_range(e.attack_range(), unit.location):
            return e, True
    return None, False


def go_blink(gc, unit, loc):
    enemycenter = Globals.radar.get_enemy_center(loc.planet)
    d = bc.Direction.North
    for i in range(8):
        if check_blink_location(gc, unit, enemycenter):
            return
        enemycenter = enemycenter.add(d)


def check_blink_location(gc, unit, destination):
    if gc.can_blink(unit.id, destination):
        nearby = gc.sense_nearby_units_by_team(destination, 2, Globals.them)
        if len(nearby) > 0:
            gc.blink(unit.id, destination)
            return True
    return False

        
        

