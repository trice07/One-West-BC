import battlecode as bc
import Globals
import Navigation
import Knight
import Ranger
import Mage



def manage_healers(gc, unit):
    """
    Runs all of the healers. Takes in a GameController object and a unit as
    inputs.
    """
    location = unit.location
    violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
    if location.is_on_map() and not location.is_in_garrison():
        nearby_units = gc.sense_nearby_units(location.map_location(), unit.vision_range)
        gc.is_overcharge_ready(unit.id)
        to_heal = None
        retreat_from = None
        found = False
        for patient in nearby_units:
            if unit.team == Globals.them:
                Globals.radar.update_enemy_cache(patient)
                if patient.unit_type in violent_enemies and patient.location.is_within_range(patient.attack_range(), unit.location) and gc.is_move_ready(unit.id):
                    retreat_from = patient
                    break
            elif gc.can_heal(unit.id, patient.id) and patient.health < patient.max_health and gc.is_heal_ready(unit.id):
                if patient.unit_type != bc.UnitType.Worker:
                    to_heal = patient
                    found = True
                elif not found:
                    to_heal = patient
        if retreat_from is not None:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, retreat_from.location.map_location())
            if moved:
                return
        if to_heal is not None:
            if gc.is_overcharge_ready(unit.id) and gc.can_overcharge(unit.id, to_heal.id):
                print("OVERCHARGING")
                gc.overcharge(unit.id, to_heal.id)
                run_turn(gc, to_heal)
                return
            gc.heal(unit.id, to_heal.id)
            return

    if gc.is_move_ready(unit.id):
        if gc.is_heal_ready(unit.id):
            planet = location.map_location().planet
            path = Globals.updatePath if planet == bc.Planet.Earth else Globals.updatePathMars
            Navigation.path_with_bfs(gc, unit, path)


# def healer_retreat(unit, dangerous_enemies):
#     violent_enemies = [bc.UnitType.Ranger, bc.UnitType.Mage, bc.UnitType.Knight]
#     for e in dangerous_enemies:
#         if e.unit_type in violent_enemies and e.location.is_within_range(e.vision_range, unit.location):
#             return e, True
#     return None, False


def run_turn(gc, unit):
    if unit.unit_type == bc.UnitType.Knight:
        return Knight.turn(gc, unit)
    if unit.unit_type == bc.UnitType.Ranger:
        return Ranger.turn(gc, unit)
    if unit.unit_type == bc.UnitType.Mage:
        return Mage.manage_mages(gc, unit)
