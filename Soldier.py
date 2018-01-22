import battlecode as bc
import random

import Move

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective

def manage_soldiers(gc, unit, my_team, enemy_center):
    """
    Runs all of the soldiers. Takes in a GameController object and a unit as
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
    
    if unit.unit_type==bc.UnitType.Healer: #Healer actions
        weakest_unit=find_weakest_unit(gc)
        if isinstance(weakest_unit, bc.Unit): #If there is a weakest unit on the map
            if gc.can_heal(unit.id, weakest_unit.id) and gc.is_heal_ready(unit.id): #Try to heal it and if it cant, move towards it and try to heal until it is no longer the weakest unit on the map
                gc.heal(unit.id, weakest_unit.id)
            Move.Bug(gc, unit, weakest_unit.map_location())
        else: #If there are no units that can be healed, the healer moves randomly
            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
              
    if unit.unit_type==bc.UnitType.Knight: #Knight actions
        nearby=gc.sense_nearby_units_by_team(location.map_location(), 50, enemy_team)
        if len(nearby)==0:
            if unit in arrived: #If the unit has already moved to the center of the enmy position, move randomly until it detects something
                random_movement(gc, unit, direction)
            else: #If the unit has not gone to the enemy center yet
                Move.Bug(gc, unit, enemy_center)
                if unit.location.map_location().distance_squared_to(enemy_center)<4: #Check to see if it is within two squares of the enemy center
                    arrived.append(unit)
        else:
            for other in nearby: #Loop through units in the vision range and see if they can be attacked
                if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
                    gc.attack(unit.id, other.id)
                else: #Otherwise, find the closest one and move towards it and check if you can attack
                    closest=find_closest_target(unit, nearby, my_team)
                    Move.Bug(gc, unit, closest)
        
    if unit.unit_type==bc.UnitType.Mage: #Mage actions
        nearby=gc.sense_nearby_units_by_team(location.map_location(), 30, enemy_team)
        if len(nearby)==0:
            if unit in arrived: #If the unit has already moved to the center of the enmy position, move randomly until it detects something
                random_movement(gc, unit, direction)
            else: #If the unit has not gone to the enemy center yet
                Move.Bug(gc, unit, enemy_center)
                if unit.location.map_location().distance_squared_to(enemy_center)<4: #Check to see if it is within two squares of the enemy center
                    arrived.append(unit)
        else:
            for other in nearby: #Loop through units in the vision range and see if they can be attacked
                if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
                    gc.attack(unit.id, other.id)
                else: #Otherwise, find the closest one and move towards it and check if you can attack
                    closest=find_closest_target(unit, nearby, my_team)
                    Move.Bug(gc, unit, closest)

    if unit.unit_type==bc.UnitType.Ranger: #Ranger actions
        nearby=gc.sense_nearby_units_by_team(location.map_location(), 70, enemy_team)
        if len(nearby)==0:
            if unit in arrived: #If the unit has already moved to the center of the enmy position, move randomly until it detects something
                random_movement(gc, unit, direction)
            else: #If the unit has not gone to the enemy center yet
                Move.Bug(gc, unit, enemy_center)
                if unit.location.map_location().distance_squared_to(enemy_center)<4: #Check to see if it is within two squares of the enemy center
                    arrived.append(unit)
        else:
            for other in nearby: #Loop through units in the vision range and see if they can be attacked
                if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
                    gc.attack(unit.id, other.id)
                else: #Otherwise, find the closest one and move towards it and check if you can attack
                    closest=find_closest_target(unit, nearby, my_team)
                    Move.Bug(gc, unit, closest)
        
def random_movement(gc, unit, direction):
    """
    Moves the robot in a random direction. Takes a GameController object, a unit,
    and a direction as inputs.
    """
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
        gc.move_robot(unit.id, direction)

def find_closest_target(unit, nearby, my_team):
        best=None
        target=None
        me=unit.location.map_location()
        for enemy in nearby:
            if enemy.team!=my_team:
                them=enemy.location.map_location()
                distance=me.distance_squared_to(them)
                if best==None or distance<best:
                    best=distance
                    target=them
        return target
    

def find_weakest_unit(gc):
    """
    Returns the the unit on the map with the weakest health. Takes a
    GameController object as input.
    """
    weakest_health=250 #The highest possible max health
    weakest_unit=None
    for unit in gc.my_units():
        if unit.unit_type!=bc.UnitType.Factory and unit.unit_type!=unit.unit_type.Rocket: #If the unit is a soldier
            if unit.health<unit.max_health and unit.health<weakest_health: #If the units health is below the max and below the weakest health on the board
                weakest_health=unit.health
                weakest_unit=unit
    return weakest_unit
