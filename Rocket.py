import battlecode as bc
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed

def manage_rockets(gc, unit, mars_width, mars_height):
    """
    """
    location=unit.location

    if location.map_location().planet == bc.Planet.Earth:
        print(unit.id, "ROCKET ON MAP")
        if unit.structure_is_built():
            print(unit.id, "ROCKET IS BUILT")
        if len(unit.structure_garrison())>0:
            destination=find_landing(gc, mars_width, mars_height)
            if gc.can_launch_rocket(unit.id, destination):
                print(unit.id, "ROCKET CAN LAUNCH")
                gc.launch_rocket(unit.id, destination)
    else:
        d = random.choice(bc.Direction)
        if gc.can_unload(unit.id, d):
            gc.unload(unit.id, d)



def find_landing(gc, mars_width, mars_height):
    """
    """
    mars_map=gc.starting_map(bc.Planet.Mars)
    x=random.randint(0, mars_width-1)
    y=random.randint(0, mars_height-1)
    location=bc.MapLocation(bc.Planet.Mars, x, y)
    while not mars_map.is_passable_terrain_at(location):
        x=random.randint(0, mars_width-1)
        y=random.randint(0, mars_height-1)
        location=bc.MapLocation(bc.Planet.Mars, x, y)
    return location
