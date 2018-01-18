import battlecode as bc
import Move
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective

def manage_mages(gc, unit, enemy_center, enemy_map, enemy_team):
    """
    Runs all of the mages. Takes in a GameController object, a unit,
    the starting center of enemy activity, an enemy_map, and the enemy
    team as inputs.
    """
    global arrived
    location=unit.location #Gets the units location
    direction=random.choice(directions) #Picks a direction
    while direction==bc.Direction.Center: #Ensures that the direction is not center
        direction=random.choice(directions)          
    closest=Move.find_closest_target(unit, enemy_map, unit.location.map_location().planet) #The closest known enemy unit 
    nearby=gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), enemy_team) #All units that can be attacked 
    if unit in arrived: #If the unit has already moved to the center of the enemy position, move to the nearest known enemy or move randomly if there are none
        if len(nearby)==0: #If there are no nearby units
            if closest==None: #If there is no closest location (Arbitrary impossible position used to represent None) move randomly
                Move.random_movement(unit, direction) 
            else: #Otherwise, move to the closest known unit
                Move.Bug(gc, unit, closest)
        else:
            for other in nearby:
                if gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                    gc.attack(unit.id, other.id)
            Move.Bug(gc, unit, other.location.map_location())
    else:  #If the unit has not yet arrived, move towards the target point until it sees something else then move to attack it 
        if unit.location.map_location().distance_squared_to(enemy_center)<25: #If the enemy is within five squares of the center of enemy activity
            arrived.append(unit)
        if len(nearby)>0: #If there are nearby units loop through them
            for other in nearby:
                if gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can be attacked and we are ready to attack, attack it
                    gc.attack(unit.id, other.id)
            Move.Bug(gc, unit, other.location.map_location()) #Then move in its direction
        else: #Otherwise, move towards the maps center
            Move.Bug(gc, unit, enemy_center)






        
        

