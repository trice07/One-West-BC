import battlecode as bc
import Units
import Globals
import Navigation


def manage_healers(gc, unit):
    """
    Runs all of the healers. Takes in a GameController object and a unit as
    inputs.
    """
    nearby_units = None
    enemy_units = []
    location = unit.location
    if unit.location.is_on_map() and not location.is_in_garrison() and gc.is_heal_ready(unit.id):
        nearby_units = gc.sense_nearby_units(location.map_location(), unit.attack_range())
        for patient in nearby_units:
            if unit.team == Globals.them:
                enemy_units.append(patient)
            elif gc.can_heal(unit.id, patient.id) and patient.health < patient.max_health:
                gc.heal(unit.id, patient.id)
                return

    if enemy_units == []:
        enemy_units = Globals.radar.update_radar(gc, unit)
    if gc.is_move_ready(unit.id):
        should_retreat = Units.try_to_retreat(unit, enemy_units)
        if should_retreat:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, Globals.radar.get_enemy_center(unit.location.map_location().planet))
            if moved:
                return
        Navigation.path_with_bfs(gc, unit)
