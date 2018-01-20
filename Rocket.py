import battlecode as bc
import Globals
import random

directions = list(bc.Direction)  # Stores all directions as a list
random.seed(1)  # Random seeding for testing. Will be removed


def manage_rockets(gc, unit):
    """
    """
    location = unit.location

    if location.map_location().planet == bc.Planet.Earth:
        print(unit.id, "ROCKET ON MAP")
        if unit.structure_is_built():
            print(unit.id, "ROCKET IS BUILT")
        if len(unit.structure_garrison()) > 4:
            destination = find_landing(gc, unit)
            if destination is not None:
                print(unit.id, "ROCKET CAN LAUNCH")
                gc.launch_rocket(unit.id, destination)
    else:
        d = random.choice(bc.Direction)
        if gc.can_unload(unit.id, d):
            gc.unload(unit.id, d)


def find_landing(gc, unit):
    """
    """
    mars_map = Globals.radar.mars_map
    for l in mars_map:
        ml = bc.MapLocation(bc.Planet.Mars, l[0], l[1])
        if gc.can_launch_rocket(unit.id, ml):
            return ml
    return None
