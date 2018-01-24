import battlecode as bc
import random

import Globals
import WorkerMovement
import Navigation

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed


def manage_worker(gc, unit):
    """
    Runs all of the workers actions. Takes in a GameController object, a unit,
    the list of factories, and the list of rockets as inputs.
    """
    #earth worker logic
    loc = unit.location.map_location()
    h, bf, br, r = findViableDirection(gc, unit)
    if loc.planet == bc.Planet.Earth:
        karb = WorkerMovement.findNearestKarb(gc, unit)
        # declot(gc, loc, unit, karb)
        width = Globals.earth_width
        height = Globals.earth_height
        if Globals.radar.our_num_earth_workers < Globals.REPLICATE_UNTIL:
            if len(r) != 0:
                gc.replicate(unit.id, r[0])
                return

        nearby = gc.sense_nearby_units(loc, 2)
        count = 0
        for other in nearby:
            # otherloc = other.location.map_location()
            # direction = loc.direction_to(otherloc)
            if other.unit_type == bc.UnitType.Rocket or other.unit_type == bc.UnitType.Factory:
                if gc.can_build(unit.id, other.id):
                    gc.build(unit.id, other.id)
                    count += 1
                    return
                # elif not other.structure_is_built():
                #     if gc.is_move_ready(unit.id):
                #         if gc.can_move(unit.id, direction):
                #             gc.move_robot(unit.id, direction)
                #             return
                elif other.health < other.max_health / 4:
                    if gc.can_repair(unit.id, other.id):
                        gc.repair(unit.id, other.id)
                        return
                elif other.unit_type == bc.UnitType.Worker:
                    count += 1
                # else:
                #     if gc.is_move_ready(unit.id):
                #         if gc.can_move(unit.id, direction):
                #             gc.move_robot(unit.id, direction)
                #             return

        declot(gc, unit, count, width, height, karb)

        if Globals.radar.our_num_earth_factories < 5:
            if len(bf) == 0:
                if len(h) != 0:
                    gc.harvest(unit.id, h[0])
                    return
                elif karb is not None:
                    d = loc.direction_to(karb)
                    if gc.can_replicate(unit.id, d) and Globals.radar.our_num_earth_workers < 25:
                        gc.replicate(unit.id, d)
                        return
            else:
                gc.blueprint(unit.id, bc.UnitType.Factory, bf[0])
                return

        if gc.round() > 100:
            if Globals.radar.our_num_mars_rangers < 10 or Globals.radar.our_num_mars_workers < 5:
                if len(br) == 0:
                    if gc.is_move_ready(unit.id):
                        Navigation.Bug(gc, unit, karb)
                        return
                else:
                    gc.blueprint(unit.id, bc.UnitType.Rocket, br[0])

        # d = findViableDirection(gc, unit, "harvest")
        # if d is None:
        #     karbDir = loc.direction_to(karb)
        #     if gc.can_replicate(unit.id, karbDir) and gc.karbonite() > 150:
        #         gc.replicate(unit.id, karbDir)
        #     elif gc.is_move_ready(unit.id):
        #         Navigation.Bug(gc, unit, karb)
        #         return
        # else:
        #     gc.harvest(unit.id, d)

    #mars worker logic
    elif loc.planet == bc.Planet.Mars:
        karb = WorkerMovement.findNearestKarb(gc, unit)
        if Globals.radar.their_num_mars_rockets > 0 or gc.round() > 700:
            if len(r) == 0:
                if gc.is_move_ready(unit.id) and karb is not None:
                    Navigation.Bug(gc, unit, karb)
                    return
            else:
                gc.replicate(unit.id, r[0])
        else:
            if gc.is_move_ready(unit.id):
                Navigation.Bug(gc, unit, karb)


def declot(gc, unit, count, width, height, desloc):
    loc = unit.location.map_location()
    if count > 4:
        if gc.is_move_ready(unit.id):
            Navigation.Bug(gc, unit, desloc)
    if loc.x == 0 or loc.x == width or loc.y == 0 or loc.y == height:
        if count > 2:
            if gc.is_move_ready(unit.id):
                Navigation.Bug(gc, unit, desloc)


def findViableDirection(gc, unit, d=random.choice(directions)):
    h = []
    bf = []
    br = []
    r = []
    center_check = True
    for i in range(8):
        if gc.can_harvest(unit.id, bc.Direction.Center) and center_check:
            h.append(bc.Direction.Center)
            center_check = False
        elif gc.can_harvest(unit.id, d):
            h.append(d)
        if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
            bf.append(d)
        if gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
            br.append(d)
        if gc.can_replicate(unit.id, d):
            r.append(d)
        d = d.rotate_right()
    return h, bf, br, r


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
