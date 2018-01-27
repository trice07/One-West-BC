import battlecode as bc
import Navigation
import Globals


def shoot_at_best_target(gc, unit):
    """
    :param: unit: Unit : unit that is shooting
    :return: bool: true if shot, false if not
    """
    if not gc.is_attack_ready(unit.id):
        return None
    closest_target = get_best_target(gc, unit)
    if isinstance(closest_target, bc.Unit):
        gc.attack(unit.id, closest_target.id)
    return closest_target


def get_best_target(gc, unit):
    """
    Gets the best target a unit can shoot at
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    planet = unit.location.map_location().planet
    if planet == bc.Planet.Earth:
        return get_best_target_earth(gc, unit)
    elif planet == bc.Planet.Mars:
        return get_best_target_mars(gc, unit)
    return None


def get_best_target_earth(gc, unit):
    """
    Gets the best target a unit can shoot at on Earth
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    for enemy in Globals.radar.being_shot_at_earth:
        if gc.can_attack(unit.id, enemy.id):
            if enemy.health <= unit.damage():
                Globals.radar.being_shot_at_earth.remove(enemy)
                Globals.radar.delete_enemy_from_radar(enemy)
            return enemy
    target_list = Globals.radar.update_radar(gc, unit)
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            if target.health <= unit.damage():
                Globals.radar.delete_enemy_from_radar(target)
            else:
                Globals.radar.being_shot_at_earth.append(target)
            return target
    return target_list


def get_best_target_mars(gc, unit):
    """
    Gets the best target a unit can shoot at on Mars
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    for enemy in Globals.radar.being_shot_at_mars:
        if gc.can_attack(unit.id, enemy.id):
            if enemy.health <= unit.damage():
                Globals.radar.being_shot_at_mars.remove(enemy)
                del Globals.radar.mars_enemy_locations[enemy.id]
            return enemy
    target_list = Globals.radar.update_radar(gc, unit)
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            return target
    return target_list


def try_go_to_rocket(gc, unit):
    if unit.id in Globals.rockets_queue and gc.is_move_ready(unit.id) and not unit.location.is_in_garrison():
        rocket_location = Globals.rockets_queue[unit.id].location
        rocket_id = Globals.rockets_queue[unit.id].id
        if gc.can_load(rocket_id, unit.id):
            Globals.rockets_waiting[rocket_id]["units_ready"].add(unit.id)
            return True
        destination = rocket_location.map_location()
        Navigation.Bug(gc, unit, destination)
        return True
    return False

