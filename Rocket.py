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
    if location.is_on_map():
        if len(unit.structure_garrison())>0:
            destination=find_landing(mars_width, mars_height, mars_passable_map)
            if gc.can_launch_rocket(unit.id, destination):
                gc.launch_rocket(unit.id, destination)

def find_landing(mars_width, mars_height, passable_mars_map):
    """

    """
    i=random.choice(list(passable_mars_map))
    while passable_mars_map[i]==False:
       i=random.choice(list(passable_mars_map))
    return bc.MapLocation(bc.Planet.Mars, i[0], i[1])
