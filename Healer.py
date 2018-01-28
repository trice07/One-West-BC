import battlecode as bc
import Units
import Globals
import Navigation


def manage_healers(gc, unit):
    """
    Runs all of the healers. Takes in a GameController object and a unit as
    inputs.
    """
    enemy_units = []
    location = unit.location
    if unit.location.is_on_map() and not location.is_in_garrison() and gc.is_heal_ready(unit.id):
        nearby_units = Globals.radar.update_radar(gc, unit, unit.attack_range())
        for patient in nearby_units:
            if unit.team == Globals.them:
                enemy_units.append(patient)
            elif gc.can_heal(unit.id, patient.id) and patient.health < patient.max_health:
                gc.heal(unit.id, patient.id)
                return

    if len(enemy_units) == 0:
        enemy_units = Globals.radar.update_radar(gc, unit)
    if gc.is_move_ready(unit.id):
        e, should_retreat = healer_retreat(unit, enemy_units)
        if should_retreat:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, e.location.map_location())
            if moved:
                return
        planet = location.map_location().planet
        path = Globals.pathToEnemy if planet == bc.Planet.Earth else Globals.pathToEnemyMars
        Navigation.path_with_bfs(gc, unit, path)


def healer_retreat(unit, dangerous_enemies):
    violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
    for e in dangerous_enemies:
        if e.unit_type in violent_enemies and e.location.is_within_range(e.attack_range(), unit.location):
            return e, True
    return None, False
