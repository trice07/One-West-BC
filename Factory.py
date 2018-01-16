import battlecode as bc
import random

directions=list(bc.Direction) #Stores all directions as a list
  
def factory_manager(gc, unit, factories, rockets, soldiers, workers):
    """
    Handles a factory unit and how it operates each turn. Takes a
    GameController, a unit, and lists of all factories, soldiers, and workers
    as inputs.
    """
    num_earth_workers=get_earth_units(gc, [bc.UnitType.Worker]) #Gets the total number of workers on Earth and in garrisons
    garrison=unit.structure_garrison() #Gets the unit garrison
    if len(garrison)>0 or (gc.round()>125 and gc.karbonite()<bc.UnitType.Rocket.blueprint_cost() and len(rockets)<5): #If there is a unit in the garrison or there is less money than required to build a rocket, unload the garrison
        random_unload(gc, unit)
    elif len(garrison)<6: #Never let the garrison have more than six units in it. Ensures a constant stream as it takes five turns to build a unit
        if num_earth_workers==0: #If there are no workers left or there are three times as many soldiers, produce a worker
            if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
                gc.can_produce_robot(unit.id, bc.UnitType.Worker)
        else: #If there are fewer than three times as many soldiers then produce a knight 
            if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                gc.produce_robot(unit.id, bc.UnitType.Knight)

def get_earth_units(gc, unit_types):
    """
    Returns the total number of units of a given type that are on Earth or in
    a garrison. Takes a GameController and a list of unit types as inputs.
    """
    num_units=0 #The return value
    for unit in gc.my_units():
        if unit.location.is_in_garrison or unit.location.map_location().planet==bc.Planet.Earth: #If the unit exists or is in a garrison
            num_units+=1
    return num_units

def random_unload(gc, factory):
    """
    Tries to unload a unit in a random direction. Takes in a GameController
    object and a factory as inputs.
    """
    direction=random.choice(directions)
    while direction==bc.Direction.Center: #Never unload to the center
        direction=random.choice(directions)
    if gc.can_unload(factory.id, direction): #Unload a unit in a random direction
        gc.unload(factory.id, direction)
