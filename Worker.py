import battlecode as bc
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed

def manage_worker(gc, unit):
    """
    Runs all of the workers actions. Takes in a GameController object and a unit
    as inputs.
    """
    location=unit.location #Gets the units location
    num_factories=get_num_factories(gc) #Counts the total number of factories
    num_rockets=get_num_rockets(gc) #Counts the total number of rockets
    direction=random.choice(directions) #Sets the direction for the unit to move
    while direction==bc.Direction.Center: #Ensures thatthe direction is not center
        direction=random.choice(directions)
    if location.is_on_map(): #As long as the unit is not in a garrison or in space
        nearby=gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby: #Loops through all nearby units
            if gc.can_build(unit.id, other.id) or gc.can_repair(unit.id, other.id): #If the unit can be built or repaired
                if gc.can_build(unit.id, other.id): #If the unit needs to be built
                    gc.build(unit.id, other.id)
                elif gc.can_repair(unit.id, other.id): #If the unit needs to be repaired
                    gc.repair(unit.id, other.id)
                if other.health!=other.max_health: #If the unit isnt fully built yet, dont let the worker move
                    direction=bc.Direction.Center
            if other.unit_type==bc.UnitType.Rocket and num_factories>=3 and num_rockets>=5:
                if gc.can_load(other.id, unit.id):
                    gc.load(other.id, unit.id)
                        
        if num_factories<3: #If there are fewer than three factories, build one where the robot is
            if gc.karbonite()>bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, direction):
                if len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 4, bc.UnitType.Factory))==0: #If there is not another factory within two spaces, blueprint a factory there
                    gc.blueprint(unit.id, bc.UnitType.Factory, direction)
            if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
                gc.harvest(unit.id, direction)
            else: #Otherwise, move randomly
                random_movement(gc, unit, direction)
                    
        elif gc.round()>125 and num_rockets<5: #If rocketry has been researched and there are less than 5 rockets on the map
            if gc.karbonite()>bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, direction): #If a rocket can be built
                if len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 2, bc.UnitType.Factory))==0 and len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 2, bc.UnitType.Rocket))==0: #If there is not a factory or a rocket within one space, blueprint a rocket there
                    gc.blueprint(unit.id, bc.UnitType.Rocket, direction)
            if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
                gc.harvest(unit.id, direction)
            else: #Otherwise, move randomly
                random_movement(gc, unit, direction)
                
        else: #Otherwise
            if gc.round()%50==0: #If the round is a multiple of 50, try to replicate the worker
                if gc.can_replicate(unit.id, direction):
                    gc.replicate(unit.id, direction)
            if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
                gc.harvest(unit.id, direction)
            else: #Otherwise, move randomly
                random_movement(gc, unit, direction)

def get_num_factories(gc):
    """
    Returns the number of factories. Seperate from len(factories) as that does not
    update until the end of a turn.
    """
    num_factories=0
    for unit in gc.my_units(): #Loops through all units on team
        if unit.unit_type==bc.UnitType.Factory: #Checks to see if they are factories
            num_factories+=1
    return num_factories

def get_num_rockets(gc):
    """
    Returns the number of factories. Seperate from len(factories) as that does not
    update until the end of a turn.
    """
    num_rockets=0
    for unit in gc.my_units(): #Loops through all units on team
        if unit.unit_type==bc.UnitType.Rocket: #Checks to see if they are rockets
            num_rockets+=1
    return num_rockets

def random_movement(gc, unit, direction):
    """
    Moves the robot in a random direction. Takes a GameController object, a unit,
    and a direction as inputs.
    """
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
        gc.move_robot(unit.id, direction)
