import battlecode as bc
import Globals
import Navigation


def manage_healers(gc, unit):
    """
    Runs all of the healers. Takes in a GameController object and a unit as
    inputs.
    """
    enemy_units = []
    location = unit.location
    if location.is_on_map() and gc.is_heal_ready(unit.id) and not location.is_in_garrison():
        nearby_units = gc.sense_nearby_units(location.map_location(), unit.vision_range)
        to_heal = None
        for patient in nearby_units:
            if unit.team == Globals.them:
                enemy_units.append(patient)
                Globals.radar.update_enemy_cache(patient)
            elif gc.can_heal(unit.id, patient.id) and patient.health < patient.max_health:
                to_heal = patient
                if to_heal.unit_type != bc.UnitType.Worker:
                    break
        if to_heal is not None:
            gc.heal(unit.id, to_heal.id)

    if gc.is_move_ready(unit.id):
        e, should_retreat = healer_retreat(unit, enemy_units)
        if should_retreat:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, e.location.map_location())
            if moved:
                return
        if gc.is_heal_ready(unit.id):
            planet = location.map_location().planet
            path = Globals.updatePath if planet == bc.Planet.Earth else Globals.updatePathMars
            Navigation.path_with_bfs(gc, unit, path)


def healer_retreat(unit, dangerous_enemies):
    violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
    for e in dangerous_enemies:
        if e.unit_type in violent_enemies and e.location.is_within_range(e.vision_range, unit.location):
            return e, True
    return None, False
