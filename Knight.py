import battlecode as bc
import Move
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective

def manage_knights(gc, unit, my_team, enemy_center):
    """
    Runs all of the knights. Takes in a GameController object and a unit as
    inputs.
    """
    global arrived
    location=unit.location #Gets the units location
    direction=random.choice(directions) #Picks a direction
    enemy_team=None
    while direction==bc.Direction.Center: #Ensures that the direction is not center
        direction=random.choice(directions)
    if my_team==bc.Team.Red: #Sets the value of the enemy team
        enemy_team=bc.Team.Blue
    else:
        enemy_team=bc.Team.Red           
    nearby=gc.sense_nearby_units_by_team(location.map_location(), 50, enemy_team)
    if len(nearby)==0:
        if unit in arrived: #If the unit has already moved to the center of the enmy position, move randomly until it detects something
            Move.random_movement(gc, unit, direction)
        else: #If the unit has not gone to the enemy center yet
            Move.Bug(gc, unit, enemy_center)
            if unit.location.map_location().distance_squared_to(enemy_center)<4: #Check to see if it is within two squares of the enemy center
                arrived.append(unit)
    else:
        for other in nearby: #Loop through units in the vision range and see if they can be attacked
            if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
                gc.attack(unit.id, other.id)
            else: #Otherwise, find the closest one and move towards it and check if you can attack
                closest=Move.find_closest_target(unit, nearby, my_team)
                Move.Bug(gc, unit, closest)
        
        
