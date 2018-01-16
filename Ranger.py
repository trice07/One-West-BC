import battlecode as bc
<<<<<<< HEAD
import Navigation
from Radar import Radar
import run


def send_radar_info(unit, gc):
    nearby_enemies = run.Glob.radar.update_radar(gc, unit)
    return nearby_enemies


def try_to_retreat(unit, dangerous_enemies):
    ah_time_to_run = False
    for e in dangerous_enemies:
        if e.unit_type == bc.UnitType.Ranger:
            ah_time_to_run = True
            break
        elif e.unit_type == bc.UnitType.Knight:
            if unit.location.is_within_range(1, e.location):
                ah_time_to_run = True
                break
        elif e.unit_type == bc.UnitType.Mage:
            if unit.location.is_within_range(30, e.location):
                ah_time_to_run = True
                break
    if ah_time_to_run:
        return True
    return False


def kill(unit, nearby_enemies, gc):
    if not gc.is_attack_ready:
        return False
    best = None
    priority = 5
    for e in nearby_enemies:
        if e.unit_type == bc.UnitType.Worker:
            if gc.can_attack(unit.id, e.id):
                best = e.id
                priority = 0
                break
        elif e.unit_type == bc.UnitType.Healer:
            if gc.can_attack(unit.id, e.id):
                if priority > 1:
                    priority = 1
                    best = e.id
        elif e.unit_type == bc.UnitType.Ranger:
            if gc.can_attack(unit.id, e.id):
                if priority > 2:
                    priority = 2
                    best = e.id
        elif e.unit_type == bc.UnitType.Mage:
            if gc.can_attack(unit.id, e.id):
                if priority > 3:
                    priority = 3
                    best = e.id
        elif e.unit_type == bc.UnitType.Ranger:
            if gc.can_attack(unit.id, e.id):
                if priority > 4:
                    priority = 4
                    best = e.id
    if best is None:
        return False
    gc.attack(unit.id, best)
    return True


def round(unit, gc):
    nearby_enemies = send_radar_info(unit, gc)
    if try_to_retreat(unit, nearby_enemies):
        Navigation.retreat(gc, unit)
        return
    if kill(unit, nearby_enemies, gc):
        print("Popped")
        return

    # NEEF DESTINATION IN LINE BELOW
    # Navigation.Bug(gc, destination)





=======
import Move
import random

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective

def manage_rangers(gc, unit, my_team, enemy_center):
    """
    Runs all of the rangers. Takes in a GameController object and a unit as
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
    nearby=gc.sense_nearby_units_by_team(location.map_location(), 70, enemy_team)
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
>>>>>>> 5a92a9e50500daca225581f0e2b99a65358087bf
