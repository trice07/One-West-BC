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
        if unit.unit_type == bc.UnitType.Knight:
            return get_best_target_earth_knight(gc, unit)
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
    for enemy_id in Globals.radar.being_shot_at_earth:
        if gc.can_attack(unit.id, enemy_id):
            health = Globals.radar.being_shot_at_earth[enemy_id]
            if health <= unit.damage():
                del Globals.radar.being_shot_at_earth[enemy_id]
                Globals.radar.delete_enemy_from_radar(gc.unit(enemy_id))
            else:
                Globals.radar.being_shot_at_earth[enemy_id] -= unit.damage()
            return gc.unit(enemy_id)
    target_list = Globals.radar.update_radar(gc, unit)
    best = None
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            if target.unit_type != bc.UnitType.Worker:
                best = target
                break
            else:
                best = target

    if best is not None:
        if best.health <= unit.damage():
            Globals.radar.delete_enemy_from_radar(best)
        else:
            Globals.radar.being_shot_at_earth[best.id] = (best.health - unit.damage())
        return best
    return target_list


def get_best_target_mars(gc, unit):
    """
    Gets the best target a unit can shoot at on Mars
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    for enemy_id in Globals.radar.being_shot_at_mars:
        if gc.can_attack(unit.id, enemy_id):
            health = Globals.radar.being_shot_at_mars[enemy_id]
            if health <= unit.damage():
                del Globals.radar.being_shot_at_mars[enemy_id]
                Globals.radar.delete_enemy_from_radar(gc.unit(enemy_id))
            else:
                Globals.radar.being_shot_at_mars[enemy_id] -= unit.damage()
            return gc.unit(enemy_id)
    target_list = Globals.radar.update_radar(gc, unit)
    best = None
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            if target.unit_type != bc.UnitType.Worker:
                best = target
                break
            else:
                best = target

    if best is not None:
        if best.health <= unit.damage():
            Globals.radar.delete_enemy_from_radar(best)
        else:
            Globals.radar.being_shot_at_mars[best.id] = (best.health - unit.damage())
        return best
    return target_list


def try_go_to_rocket(gc, unit):
    if unit.location.is_in_garrison():
        return True
    for f in Globals.rockets_queue:
        if unit.id in Globals.rockets_queue[f]:
            if gc.is_move_ready(unit.id):
                x = Navigation.path_with_bfs(gc, unit, Globals.rockets_queue[f][unit.id])
                return True


def get_best_target_earth_knight(gc, unit):
    """
    Gets the best target a unit can shoot at on Earth
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    target_list = Globals.radar.update_radar(gc, unit)
    best = None
    being_shot_at = False
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            if target.unit_type == bc.UnitType.Factory:
                best = target
                break
            elif target.id in Globals.radar.being_shot_at_earth:
                being_shot_at = True
                best = target
            elif being_shot_at is False:
                best = target
    if best is not None:
        if best.health <= unit.damage():
            Globals.radar.delete_enemy_from_radar(best)
            l = Globals.radar.get_coordinates(best.location.map_location())
            if l in Globals.pathToFactory:
                del Globals.pathToFactory[l]
        else:
            Globals.radar.being_shot_at_earth[best.id] = (best.health - unit.damage())
        return best

    return target_list

def get_best_target_earth_ranger(gc, unit):
    """
    Gets the best target a unit can shoot at on Earth
    :param gc: GameController
    :param unit: Unit The player unit
    :return: Unit or None
    """
    target_list = Globals.radar.update_radar(gc, unit)
    best = None
    being_shot_at = False
    for target in target_list:
        if gc.can_attack(unit.id, target.id):
            if target.unit_type == bc.UnitType.Knight:
                best = target
                break
            elif target.id in Globals.radar.being_shot_at_earth:
                being_shot_at = True
                best = target
            elif being_shot_at is False:
                best = target
    if best is not None:
        if best.health <= unit.damage():
            Globals.radar.delete_enemy_from_radar(best)
        else:
            Globals.radar.being_shot_at_earth[best.id] = (best.health - unit.damage())
        return best

    return target_list
