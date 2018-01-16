import battlecode as bc
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed

def manage_soldiers(gc, unit, my_team):
    """
    Runs all of the soldiers. Takes in a GameController object and a unit as
    inputs.
    """
    location=unit.location #Gets the units location
    direction=random.choice(directions) #Picks a direction
    while direction==bc.Direction.Center: #Ensures that the direction is not center
        direction=random.choice(directions)
    if location.is_on_map(): #If the soldier is not garrisoned or in space
        nearby=gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby: #Loop through nearby units
            if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
                gc.attack(unit.id, other.id)
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction): #If the unit can move
            gc.move_robot(unit.id, direction)
