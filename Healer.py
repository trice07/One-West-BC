import battlecode as bc
import Move
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed

def manage_healers(gc, unit):
    """
    Runs all of the healers. Takes in a GameController object and a unit as
    inputs.
    """
    location=unit.location #Gets the units location
    direction=random.choice(directions) #Picks a direction
    while direction==bc.Direction.Center: #Ensures that the direction is not center
        direction=random.choice(directions) 
    weakest_unit=find_weakest_unit(gc)
    if isinstance(weakest_unit, bc.Unit): #If there is a weakest unit on the map
        if gc.can_heal(unit.id, weakest_unit.id) and gc.is_heal_ready(unit.id): #Try to heal it and if it cant, move towards it and try to heal until it is no longer the weakest unit on the map
            gc.heal(unit.id, weakest_unit.id)
        Move.Bug(gc, unit, weakest_unit.location.map_location())
    else: #If there are no units that can be healed, the healer moves randomly
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
            gc.move_robot(unit.id, direction)
              
def find_weakest_unit(gc):
    """
    Returns the weakest non-healer unit on the board. Takes a GameController
    object as an input.
    """
    weakest_val=250 #The max health of any possible unit
    weakest_unit=None
    for unit in gc.my_units():
        if unit.unit_type!=bc.UnitType.Healer and unit.health<unit.max_health and unit.health<weakest_val: #If the unit is not another healer and has a health below its max and the current lowest health of any unit
            weakest_val=unit.health
            weakest_unit=unit
    return weakest_unit 
