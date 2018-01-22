import battlecode as bc
import Globals
import Navigation
import Units


def send_radar_info(unit, gc):
    nearby_enemies = Globals.radar.update_radar(gc, unit)
    return nearby_enemies


def try_to_retreat(unit, dangerous_enemies):
    e = None
    for e in dangerous_enemies:
        if e.unit_type == bc.UnitType.Ranger:
            return True, e
        elif e.unit_type == bc.UnitType.Knight:
            if unit.location.is_within_range(2, e.location):
                return True, e
        elif e.unit_type == bc.UnitType.Mage:
            if unit.location.is_within_range(30, e.location):
                return True, e
        # elif e.unit_type == bc.UnitType.Factory:
        #     if unit.location.is_within_range(30, e.location):
        #         return True, e
    return False, e


def turn(gc, unit):
    result = Units.shoot_at_best_target(gc, unit)
    if isinstance(result, bc.VecUnit):
        nearby_enemies = result
    elif result is None:
        nearby_enemies = send_radar_info(unit, gc)
    elif isinstance(result, bc.Unit):
        return
    else:
        print("What the f")
        return
    if gc.is_move_ready(unit.id):
        should_retreat, enemy = try_to_retreat(unit, nearby_enemies)
        if should_retreat:
            moved = Navigation.retreatFromKnownEnemy(gc, unit, enemy)
            if moved:
                return
        destination = Globals.radar.get_enemy_center(unit.location.map_location().planet)
        if unit.location.map_location() == Globals.earth_enemy_center and len(nearby_enemies) == 0:
            for e in Globals.radar.earth_enemy_locations:
                destination = Globals.radar.earth_enemy_locations[e].location.map_location()
                break
        Navigation.Bug(gc, unit, destination)
    return


# def kill(unit, nearby_enemies, gc):
#     best = None
#     priority = 6
#     for e in nearby_enemies:
#         if e.unit_type == bc.UnitType.Worker:
#             if gc.can_attack(unit.id, e.id):
#                 best = e.id
#                 break
#         elif e.unit_type == bc.UnitType.Healer:
#             if gc.can_attack(unit.id, e.id):
#                 if priority > 1:
#                     priority = 1
#                     best = e.id
#         elif e.unit_type == bc.UnitType.Ranger:
#             if gc.can_attack(unit.id, e.id):
#                 if priority > 2:
#                     priority = 2
#                     best = e.id
#         elif e.unit_type == bc.UnitType.Mage:
#             if gc.can_attack(unit.id, e.id):
#                 if priority > 3:
#                     priority = 3
#                     best = e.id
#         elif e.unit_type == bc.UnitType.Knight:
#             if gc.can_attack(unit.id, e.id):
#                 if priority > 4:
#                     priority = 4
#                     best = e.id
#         elif e.unit_type == bc.UnitType.Factory:
#             if gc.can_attack(unit.id, e.id):
#                 if priority > 5:
#                     priority = 5
#                     best = e.id
#     if best is None:
#         return False
#     gc.attack(unit.id, best)
#     return True

# =======
# import Move
# import random
#
# directions=list(bc.Direction) #Stores all directions as a list
# random.seed(1) #Random seeding for testing. Will be removed
# arrived=[] #List of units who got close to the objective
#
# def manage_rangers(gc, unit, my_team, enemy_center):
#     """
#     Runs all of the rangers. Takes in a GameController object and a unit as
#     inputs.
#     """
#     global arrived
#     location=unit.location #Gets the units location
#     direction=random.choice(directions) #Picks a direction
#     enemy_team=None
#     while direction==bc.Direction.Center: #Ensures that the direction is not center
#         direction=random.choice(directions)
#     if my_team==bc.Team.Red: #Sets the value of the enemy team
#         enemy_team=bc.Team.Blue
#     else:
#         enemy_team=bc.Team.Red
#     nearby=gc.sense_nearby_units_by_team(location.map_location(), 70, enemy_team)
#     if len(nearby)==0:
#         if unit in arrived: #If the unit has already moved to the center of the enmy position, move randomly until it detects something
#             Move.random_movement(gc, unit, direction)
#         else: #If the unit has not gone to the enemy center yet
#             Move.Bug(gc, unit, enemy_center)
#             if unit.location.map_location().distance_squared_to(enemy_center)<4: #Check to see if it is within two squares of the enemy center
#                 arrived.append(unit)
#     else:
#         for other in nearby: #Loop through units in the vision range and see if they can be attacked
#             if other.team!=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id): #If the unit can attack
#                 gc.attack(unit.id, other.id)
#             else: #Otherwise, find the closest one and move towards it and check if you can attack
#                 closest=Move.find_closest_target(unit, nearby, my_team)
#                 Move.Bug(gc, unit, closest)
