import battlecode as bc

def get_num_units(gc, unit_type):
    """
    Creates the initial breakdown of all units based on type.
    Takes in a GameController as input.
    """
    units=[]
    for unit in gc.my_units(): #Loops through all units and categorizes them
        if unit.unit_type==unit_type and unit.location.is_on_map():
            units.append(unit)
    return units


        


