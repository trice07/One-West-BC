import battlecode as bc

def split_units(gc):
    """
    Creates the initial breakdown of all units based on type.
    Takes in a GameController as input.
    """
    factories=[]
    rockets=[]
    soldiers=[]
    workers=[]
    for unit in gc.my_units(): #Loops through all units and categorizes them
        if unit.unit_type==bc.UnitType.Factory:
            factories.append(unit)
        elif unit.unit_type==bc.UnitType.Rocket:
            rockets.append(unit)
        elif unit.unit_type==bc.UnitType.Worker:
            workers.append(unit)
        else:
            soldiers.append(unit)
    return factories, rockets, soldiers, workers

def update_units(gc):
    """
    Calls the split units function and updates the unit lists. Called at the end
    of every turn. Takes in a GameController as input.
    """
    factories, rockets, soldiers, workers=split_units(gc)
    return factories, rockets, soldiers, workers
        


