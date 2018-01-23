import battlecode as bc
import random

import Globals
import WorkerMovement

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed


def manage_worker(gc, unit):
    """
    Runs all of the workers actions. Takes in a GameController object, a unit,
    the list of factories, and the list of rockets as inputs.
    """
    #earth worker logic
    if unit.location.map_location().planet == bc.Planet.Earth:
        nearby = gc.sense_nearby_units(unit.location.map_location(), unit.vision_range)
        for other in nearby:
            if other.unit_type == bc.UnitType.Rocket or other.unit_type == bc.UnitType.Factory:
                if gc.can_build(unit.id, other.id):
                    gc.build(unit.id, other.id)
                elif other.health < other.max_health / 2 and gc.can_repair(unit.id, other.id):
                    gc.repair(unit.id, other.id)
                elif other.unit_type == bc.UnitType.Rocket and gc.can_load(other.id, unit.id):
                    gc.load(other.id, unit.id)

        if gc.round() > 100:
            if Globals.radar.our_num_mars_rangers == 0 or Globals.radar.our_num_mars_workers == 0:
                d = findViableDirection(gc, unit, "blueprintr")
                if d is None:
                    if unit.movement_heat() < 10:
                        WorkerMovement.findNearestKarb(gc, unit)
                else:
                    gc.blueprint(unit.id, bc.UnitType.Rocket, d)
                    #Globals.radar.update_unit_counts_earth()
        else:
            if gc.karbonite() < 200:
                d = findViableDirection(gc, unit, "harvest")
                if d is None:
                    if unit.movement_heat() < 10:
                        WorkerMovement.findNearestKarb(gc, unit)
                else:
                    gc.harvest(unit.id, d)

            else:
                d = findViableDirection(gc, unit, "blueprintf")
                if d is None:
                    d = findViableDirection(gc, unit, "replicate")
                    if d is None:
                        if unit.movement_heat() < 10:
                            WorkerMovement.findNearestKarb(gc, unit)
                    else:
                        gc.replicate(unit.id, d)
                        #update globals
                else:
                    gc.blueprint(unit.id, bc.UnitType.Factory, d)
                    #update globals


    # #mars worker logic
    # if unit.location.map_location().planet == bc.Planet.Mars:
    #     if Globals.radar.their_num_mars_rockets > 0 or gc.round() > 700:
    #         d = findViableDirection(gc, unit, "replicate")
    #         if d is None:
    #             if unit.movement_heat() < 10:
    #                 WorkerMovement.findNearestKarb(gc, unit)
    #         else:
    #             gc.replicate(unit.id, d)
    #     else:
    #         if unit.movement_heat() < 10:
    #             WorkerMovement.findNearestKarb(gc, unit)


def findViableDirection(gc, unit, action):
    d = random.choice(directions)
    for i in range(8):
        d= d.rotate_right()
        if action == "harvest":
            if gc.can_harvest(unit.id, d):
                return d
        if action == "blueprintf":
            if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                return d
        if action == "blueprintr":
            if gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
                return d
        if action == "replicate":
            if gc.can_replicate(unit.id, d):
                return d
    return None


#     global num_rockets
#     location=unit.location #Gets the units location
#     num_factories = Globals.radar.our_num_earth_factories #Counts the total number of factories
#     num_rockets = Globals.radar.our_num_earth_rockets + Globals.radar.our_num_mars_rockets #Counts the total number of rockets
#     direction=random.choice(directions) #Sets the direction for the unit to move
#     while direction==bc.Direction.Center: #Ensures thatthe direction is not center
#         direction=random.choice(directions)
#     nearby=gc.sense_nearby_units(location.map_location(), 2)
#     for other in nearby: #Loops through all nearby units
#         if gc.can_build(unit.id, other.id) or gc.can_repair(unit.id, other.id): #If the unit can be built or repaired
#             if gc.can_build(unit.id, other.id): #If the unit needs to be built
#                 gc.build(unit.id, other.id)
#             elif gc.can_repair(unit.id, other.id): #If the unit needs to be repaired
#                 gc.repair(unit.id, other.id)
#             if other.health!=other.max_health: #If the unit isnt fully built yet, dont let the worker move
#                 direction=bc.Direction.Center
#         if other.unit_type==bc.UnitType.Rocket and gc.can_load(other.id, unit.id):
#             gc.load(other.id, unit.id)
#     if num_factories<3: #If there are fewer than three factories, build one where the robot is
#         if gc.karbonite()>bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, direction):
#             if len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 4, bc.UnitType.Factory))==0: #If there is not another factory within two spaces, blueprint a factory there
#                 gc.blueprint(unit.id, bc.UnitType.Factory, direction)
#         if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
#             gc.harvest(unit.id, direction)
#         else: #Otherwise, move randomly
#             random_movement(gc, unit, direction)
#     elif gc.round()>125 and num_rockets<1: #If rocketry has been researched and there are less than 5 rockets on the map
#         if gc.karbonite()>bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, direction): #If a rocket can be built
#             if len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 2, bc.UnitType.Factory))==0 and len(gc.sense_nearby_units_by_type(location.map_location().add(direction), 2, bc.UnitType.Rocket))==0: #If there is not a factory or a rocket within one space, blueprint a rocket there
#                 gc.blueprint(unit.id, bc.UnitType.Rocket, direction)
#                 num_rockets+=1
#         if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
#             gc.harvest(unit.id, direction)
#         else: #Otherwise, move randomly
#             random_movement(gc, unit, direction)
#     else: #Otherwise
#         if gc.round()%50==0: #If the round is a multiple of 50, try to replicate the worker
#             if gc.can_replicate(unit.id, direction):
#                 gc.replicate(unit.id, direction)
#         if gc.can_harvest(unit.id, direction) and gc.karbonite_at(location.map_location().add(direction))>0: #Try to harvest if there is karbonite at the space
#             gc.harvest(unit.id, direction)
#         else: #Otherwise, move randomly
#             random_movement(gc, unit, direction)
#
# def random_movement(gc, unit, direction):
#     """
#     Moves the robot in a random direction. Takes a GameController object, a unit,
#     and a direction as inputs.
#     """
#     if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
#         gc.move_robot(unit.id, direction)
