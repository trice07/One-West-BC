import battlecode as bc
import Navigation
from Radar import Radar
from Globals import Globals




def send_radar_info(unit, gc):
    nearby_enemies = gc.get_team_array(gc.planet)[0].update_radar(gc, unit)
    return nearby_enemies


def try_to_retreat(unit, dangerous_enemies):
    ah_time_to_run = False
    for e in dangerous_enemies:
        if e.unit_type == bc.UnitType.Ranger:
            ah_time_to_run = True
            break
        elif e.unit_type == bc.UnitType.Knight:
            if unit.location.is_within_range(1, e.location):
                ah_time_to_run = True
                break
        elif e.unit_type == bc.UnitType.Mage:
            if unit.location.is_within_range(30, e.location):
                ah_time_to_run = True
                break
    if ah_time_to_run:
        return True
    return False


def kill(unit, nearby_enemies, gc):
    if not gc.is_attack_ready:
        return False
    best = None
    priority = 5
    for e in nearby_enemies:
        if e.unit_type == bc.UnitType.Worker:
            if gc.can_attack(unit.id, e.id):
                best = e.id
                priority = 0
                break
        elif e.unit_type == bc.UnitType.Healer:
            if gc.can_attack(unit.id, e.id):
                if priority > 1:
                    priority = 1
                    best = e.id
        elif e.unit_type == bc.UnitType.Ranger:
            if gc.can_attack(unit.id, e.id):
                if priority > 2:
                    priority = 2
                    best = e.id
        elif e.unit_type == bc.UnitType.Mage:
            if gc.can_attack(unit.id, e.id):
                if priority > 3:
                    priority = 3
                    best = e.id
        elif e.unit_type == bc.UnitType.Ranger:
            if gc.can_attack(unit.id, e.id):
                if priority > 4:
                    priority = 4
                    best = e.id
    if best is None:
        return False
    gc.attack(unit.id, best)
    return True


def round(unit, gc):
    nearby_enemies = send_radar_info(unit, gc)
    if try_to_retreat(unit, nearby_enemies):
        Navigation.retreat(gc, unit)
        return
    if kill(unit, nearby_enemies, gc):
        return

    # NEEF DESTINATION IN LINE BELOW
    # Navigation.Bug(gc, destination)





