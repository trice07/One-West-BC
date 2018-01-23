import battlecode as bc
import random
import Globals

directions = list(bc.Direction)  # Stores all directions as a list
random.seed(1)  # Random seeding for testing. Will be removed


def manage_rockets(gc, unit):

    location = unit.location

    if location.map_location().planet == bc.Planet.Earth:
        if unit.id not in Globals.rockets_waiting and unit.structure_is_built():
            call_units_to_rocket(gc, unit)
            return
        elif unit.id in Globals.rockets_waiting:
            to_remove = set()
            for astronaut in Globals.rockets_waiting[unit.id]["units_ready"]:
                gc.load(unit.id, astronaut)
                to_remove.add(astronaut)
            Globals.rockets_waiting[unit.id]["units_ready"] -= to_remove
            launch = False
            units_inside = len(unit.structure_garrison())
            Globals.rockets_waiting[unit.id]["inside"] = units_inside
            total = Globals.rockets_waiting[unit.id]["total"]
            units_left = total-units_inside
            if units_left <= Globals.ROCKET_ERROR:
                Globals.rockets_waiting[unit.id]["turns_til_launch"] -= 1
                if unit.health < Globals.ROCKET_HEALTH_MIN_IF_ALMOST_FULL:
                    launch = True
            if units_left == 0 or Globals.rockets_waiting[unit.id]["turns_til_launch"] == 0 or unit.health < Globals.ROCKET_HEALTH_MIN or launch:
                destination = find_landing(gc, unit)
                if destination is not None:
                    print("LAUNCHING")
                    gc.launch_rocket(unit.id, destination)
    else:
        d = bc.Direction.North
        for i in range(8):
            d = d.rotate_right()
            if gc.can_unload(unit.id, d):
                gc.unload(unit.id, d)
                #update units on mars
                break


def find_landing(gc, unit):
    """
    """
    mars_map = Globals.radar.mars_map
    for l in mars_map:
        ml = bc.MapLocation(bc.Planet.Mars, l[0], l[1])
        if ml not in Globals.rocket_landings and gc.can_launch_rocket(unit.id, ml):
            Globals.rocket_landings.append(ml)
            return ml
    return None


def call_units_to_rocket(gc, rocket):
    rangers = []
    workers = []
    healers = []
    mages = []
    location = rocket.location.map_location()
    nearby = gc.sense_nearby_units_by_team(location, Globals.ROCKET_DISTANCE, Globals.us)
    for u in nearby:
        if u.unit_type == bc.UnitType.Ranger:
            rangers = update_rocket_closest(rangers, u, location, Globals.NUM_ROCKET_RANGERS)
        elif u.unit_type == bc.UnitType.Worker:
            workers = update_rocket_closest(workers, u, location, Globals.NUM_ROCKET_WORKERS)
        elif u.unit_type == bc.UnitType.Healer:
            healers = update_rocket_closest(healers, u, location, Globals.NUM_ROCKET_HEALERS)
        elif u.unit_type == bc.UnitType.Mage:
            healers = update_rocket_closest(mages, u, location, Globals.NUM_ROCKET_MAGES)
    q = Globals.rockets_queue
    num_units_to_wait_for = 0
    for r in rangers:
        q[r[1].id] = rocket
        num_units_to_wait_for += 1
    for w in workers:
        q[w[1].id] = rocket
        num_units_to_wait_for += 1
    for h in healers:
        q[h[1].id] = rocket
        num_units_to_wait_for += 1
    for m in mages:
        q[m[1].id] = rocket
        num_units_to_wait_for += 1
    Globals.rockets_waiting[rocket.id] = {"total": num_units_to_wait_for,
                                          "inside": 0,
                                          "turns_til_launch": Globals.TURNS_TIL_LAUNCH,
                                          "units_ready": set()}


def update_rocket_closest(units, u, location, limit):
    distance = location.distance_squared_to(u.location.map_location())
    current = (distance, u)
    if len(units) < limit:
        units.append(current)
    else:
        worst = current
        index = None
        for r in range(len(units)):
            if worst[0] < units[r][0]:
                worst = units[r]
                index = r
        if index is not None:
            units[index] = current
    return units

