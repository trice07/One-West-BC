import battlecode as bc
import random
import Units

directions=list(bc.Direction) #Stores all directions as a list
units_produced=0 #The total number of units produced, regardless of their health

def factory_manager(gc, unit):
    """
    Handles a factory unit and how it operates each turn. Takes a
    GameController and a unit as inputs.
    """
    rockets = []
    global units_produced
    num_earth_workers=get_planet_units(gc, [Units.get_num_units(gc, bc.UnitType.Worker)], bc.Planet.Earth) #Gets the total number of workers on Earth and in Earth garrisons
    garrison=unit.structure_garrison() #Gets the unit garrison
    if len(garrison)>0 or (gc.round()>125 and gc.karbonite()<bc.UnitType.Rocket.blueprint_cost() and len(rockets)<5): #If there is a unit in the garrison or there is less money than required to build a rocket, unload the garrison
        random_unload(gc, unit)
    if gc.round()<100: #For the first 100 rounds, produce units consistently
        #if units_produced%3==0 and units_produced!=0: # Every three units, produce a Mage
            #if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
                #gc.produce_robot(unit.id, bc.UnitType.Mage)
                #units_produced+=1
        #if units_produced%5==0 and units_produced!=0: #Every 5 units produce a healer
            #if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                #gc.produce_robot(unit.id, bc.UnitType.Healer)
                #units_produced+=1
        if units_produced%2==0 and units_produced!=0: #Every 20 units produce a ranger
            if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                units_produced+=1
        # else: #Otherwise, produce knights
        if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
            gc.produce_robot(unit.id, bc.UnitType.Knight)
            units_produced+=1
    else:
        if gc.round()%5==0 and gc.karbonite()>200: #After round 100, only produce units every 5 rounds (time spent garrisoned) if we have enough to build a f
            if num_earth_workers==0: #If there are no workers left or there are three times as many soldiers, produce a worker
                if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
                    gc.can_produce_robot(unit.id, bc.UnitType.Worker)
                    #Note: Workers made do not count as units produced
            else:
                #if units_produced%3==0: # Every three units, produce a Mage
                    #if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
                        #gc.produce_robot(unit.id, bc.UnitType.Mage)
                        #units_produced+=1
                #if units_produced%5==0: #Every 5 units produce a healer
                    #if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                        #gc.produce_robot(unit.id, bc.UnitType.Healer)
                        #units_produced+=1
                if units_produced%2==0: #Every 20 units produce a ranger
                    if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                        gc.produce_robot(unit.id, bc.UnitType.Ranger)
                        units_produced+=1
                #else: #Otherwise, produce knights
                if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    units_produced+=1

def get_planet_units(gc, unit_types, planet):
    """
    Returns the total number of units of a given type that are on Earth or in
    a garrison. Takes a GameController and a list of unit types as inputs.
    """
    num_units=0 #The return value
    for i in unit_types:
        for unit in i:
            if unit.location.is_in_garrison or unit.location.map_location().planet==bc.Planet.Earth: #If the unit exists on earth or is in a garrison
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
