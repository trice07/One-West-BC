import battlecode as bc
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed

def manage_rockets(gc, unit, mars_width, mars_height, mars_passable_map):
    """

    """
    #Check unit garrison
    #Can the rocket launch
    #Rocket.unload if on Mars
    #Disentigrate the rocket
    location=unit.location

    if location.map_location().planet == bc.Planet.Earth:
        print(unit.id, "ROCKET ON MAP")
        if unit.structure_is_built():
            print(unit.id, "ROCKET IS BUILT")
        if len(unit.structure_garrison())>0:
            destination=find_landing(mars_width, mars_height, mars_passable_map)
            if gc.can_launch_rocket(unit.id, destination):
                print(unit.id, "ROCKET CAN LAUNCH")
                gc.launch_rocket(unit.id, destination)
    else:
        d = random.choice(bc.Direction)
        if gc.can_unload(unit.id, d):
            gc.unload(unit.id, d)



def find_landing(mars_width, mars_height, passable_mars_map):
    """

    """
    for i in range(mars_width):
        for j in range(mars_height):
            location = bc.MapLocation(bc.Planet.Mars, i, j)
            if passable_mars_map.is_passable_terrain_at(location):
                return location
