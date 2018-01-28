import battlecode as bc

import Globals

directions = list(bc.Direction)  # Stores all directions as a list
units_produced = 0  # The total number of units produced, regardless of their health


def factory_manager(gc, unit):
    """
    Handles a factory unit and how it operates each turn. Takes a
    GameController and a unit as inputs.
    """
    global units_produced
    garrison = unit.structure_garrison()  # Gets the unit garrison
    if len(garrison) > 0:  # If there is a unit in the garrison or there is less money than required to build a rocket, unload the garrison
        findViableDirection(gc, unit)
    # if gc.round() < 100:  # For the first 100 rounds, produce units consistently
        # if units_produced % 9 == 0 and units_produced != 0:  # Every five units, produce a Mage
        #     if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
        #         gc.produce_robot(unit.id, bc.UnitType.Mage)
        #         units_produced += 1
    if Globals.everyone_to_mars or Globals.factory_hold:
        if Globals.radar.our_num_earth_workers < 2:
            if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
                gc.produce_robot(unit.id, bc.UnitType.Worker)
                units_produced += 1
        return

    if Globals.INITIAL_DISTANCE < 10 and (len(Globals.radar.update_radar(gc, unit, 6)) > 0 or gc.round() < 80):
        if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
            gc.produce_robot(unit.id, bc.UnitType.Knight)
            units_produced += 1
            return

    if Globals.radar.our_num_earth_workers < 2 and Globals.radar.our_num_earth_rangers > 3:
        if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
            gc.produce_robot(unit.id, bc.UnitType.Worker)
            units_produced += 1
            return

    if gc.round() < 100 and Globals.radar.our_num_earth_rangers < 10:
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
            units_produced += 1
            return
    if Globals.radar.our_num_earth_healers < .5*Globals.radar.our_num_earth_rangers:
        if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
            gc.produce_robot(unit.id, bc.UnitType.Healer)
            units_produced += 1
            return
    else:
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
            gc.produce_robot(unit.id, bc.UnitType.Ranger)
            units_produced += 1
            return
    # if gc.round() % 3 == 0:  # Every two units produce a ranger
    #     if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
    #         gc.produce_robot(unit.id, bc.UnitType.Ranger)
    #         units_produced += 1
    # else:  # Otherwise, produce rangers
    #     if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
    #         gc.produce_robot(unit.id, bc.UnitType.Ranger)
    #         units_produced += 1
    # else:
    #     if gc.round() % 5 == 0:  # After round 100, only produce units every 5 rounds (time spent garrisoned) if we have enough to build a factory
    #         if num_earth_workers == 0:  # If there are no workers left or there are three times as many soldiers, produce a worker
    #             if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
    #                 gc.can_produce_robot(unit.id, bc.UnitType.Worker)
    #                 # Note: Workers made do not count as units produced
    #         else:
    #             # if units_produced % 9 == 0:  # Every five units, produce a Mage
    #             #     if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
    #             #         gc.produce_robot(unit.id, bc.UnitType.Mage)
    #             #         units_produced += 1
    #             if units_produced % 6 == 0:  # Every six units produce a healer
    #                 if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
    #                     gc.produce_robot(unit.id, bc.UnitType.Healer)
    #                     units_produced += 1
    #             if units_produced % 2 == 0:  # Every three units produce a ranger
    #                 if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
    #                     gc.produce_robot(unit.id, bc.UnitType.Ranger)
    #                     units_produced += 1
    #             else:  # Otherwise, produce rangers
    #                 if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
    #                     gc.produce_robot(unit.id, bc.UnitType.Ranger)
    #                     units_produced += 1


def findViableDirection(gc, factory):
    """
    Tries to unload a unit in a random direction. Takes in a GameController
    object and a factory as inputs.
    """
    direction = factory.location.map_location().direction_to(Globals.radar.get_enemy_center(bc.Planet.Earth))
    for i in range(8):
        direction = direction.rotate_right()
        if gc.can_unload(factory.id, direction):
            gc.unload(factory.id, direction)
            return
