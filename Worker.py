import battlecode as bc
import random
import Globals
import WorkerMovement
import Navigation

directions = list(bc.Direction) # Stores all directions as a list
random.seed(1) # Random seeding for testing. Will be removed


def manage_worker(gc, unit):
    """
    Runs all of the workers actions. Takes in a GameController object, a unit,
    the list of factories, and the list of rockets as inputs.
    """
    # earth worker logic
    loc = unit.location.map_location()
    factory_duty = Globals.workers_factory_duty
    h, bf, br, r, blue, fix = findViableDirection(gc, unit)
    if loc.planet == bc.Planet.Earth:

        if Globals.everyone_to_mars:
            if len(br) != 0:
                gc.blueprint(unit.id, bc.UnitType.Rocket, br[0])
                broadcast_building_factory(gc, loc.add(br[0]))
                return

        if len(blue) != 0:
            gc.build(unit.id, blue[0][0])
            if blue[0][1] in factory_duty and unit.id in factory_duty[blue[0][1]]:
                # print("made it to factory")
                del factory_duty[blue[0][1]][unit.id]
            return

        for f in factory_duty:
            if unit.id in factory_duty[f] and gc.is_move_ready(unit.id):
                Navigation.path_with_bfs(gc, unit, factory_duty[f][unit.id])
                # print("Going towards factory", unit.id)
                return

        if gc.round() > 250:
            if len(br) != 0:
                gc.blueprint(unit.id, bc.UnitType.Rocket, br[0])
                broadcast_building_factory(gc, loc.add(br[0]))
                return

        elif len(r) != 0:
            gc.replicate(unit.id, r[0])
            return

        if len(fix) != 0:
            # print("fixing")
            gc.repair(unit.id, fix[0])
            return

        if should_build_factory(gc) and len(bf) > 0:
            gc.blueprint(unit.id, bc.UnitType.Factory, bf[0])
            broadcast_building_factory(gc, loc.add(bf[0]))
            return

        if len(h) > 0:
            # print("harvesting")
            gc.harvest(unit.id, h[0])
            Globals.radar.update_karb_amount(gc, loc.add(h[0]))
            return

        if gc.is_move_ready(unit.id):
            # print("goin to karb")
            moved = Navigation.karbpath(gc, unit, loc)
            if moved:
                return
            else:
                for i in directions:
                    if gc.can_move(unit.id, i):
                        gc.move_robot(unit.id, i)
                        return


    # mars worker logic
    elif loc.planet == bc.Planet.Mars:
        if len(r) != 0:
            gc.replicate(unit.id, r[0])
            return

        if len(h) > 0:
            gc.harvest(unit.id, h[0])
            Globals.radar.update_karb_amount(gc, loc.add(h[0]))
            return

        if gc.is_move_ready(unit.id):
            karb_distance, karb = WorkerMovement.findNearestKarb(gc, unit)
            Navigation.Bug(gc, unit, karb)


# def declot(gc, unit, count, width, height, desloc):
#     loc = unit.location.map_location()
#     if count > 4:
#         if gc.is_move_ready(unit.id):
#             Navigation.Bug(gc, unit, desloc)
#     if loc.x == 0 or loc.x == width or loc.y == 0 or loc.y == height:
#         if count > 2:
#             if gc.is_move_ready(unit.id):
#                 Navigation.Bug(gc, unit, desloc)


def findViableDirection(gc, unit, d=random.choice(directions)):
    h = []
    bf = []
    br = []
    r = []
    blue = []
    fix = []
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
        if gc.can_replicate(unit.id, d) and should_replicate(gc, unit.id, d):
            if gc.can_harvest(unit.id, d) and len(r) > 0:
                temp = r[0]
                r[0] = d
                r.append(temp)
            else:
                r.append(d)
        nb = unit.location.map_location().add(d)
        if gc.has_unit_at_location(nb):
            poss = gc.sense_unit_at_location(nb)
            if poss.team == Globals.them:
                Globals.radar.update_enemy_cache(poss)
            if poss is not None and (poss.unit_type == bc.UnitType.Factory or poss.unit_type == bc.UnitType.Rocket):
                if gc.can_build(unit.id, poss.id):
                    blue.append((poss.id, Globals.radar.get_coordinates(nb)))
                elif gc.can_repair(unit.id, poss.id) and poss.health < poss.max_health:
                    fix.append(poss.id)
        d = d.rotate_right()
    return h, bf, br, r, blue, fix


def should_build_factory(gc):
    if gc.round() >= 1 and gc.karbonite() >= 100 and Globals.radar.our_num_earth_factories < Globals.MAX_FACTORIES:
        return True


def broadcast_building_factory(gc, factory_location):
    if Globals.radar.our_num_earth_workers >= 3:
        get_closest_workers(gc, factory_location)


def get_closest_workers(gc, start):
    map = gc.starting_map(bc.Planet.Earth)
    d = bc.Direction.North
    for i in range(8):
        loc = start.add(d)
        if map.on_map(loc):
            if map.is_passable_terrain_at(start):
                break
        start = start.add(d)
    if map.on_map(start):
        if map.is_passable_terrain_at(start):
            frontier = [start]
            parents = {(start.x, start.y): None}
            w_found = []
            count = 0

            while frontier and count < 55:
                frontier, workers, parents = exploreFrontier(frontier, map, parents, gc)
                w_found += workers
                if len(w_found) >= 3:
                    break
                count += 1
            loc_key = Globals.radar.get_coordinates(start)
            for i in range(len(w_found)):
                if loc_key in Globals.workers_factory_duty:
                    Globals.workers_factory_duty[loc_key][w_found[i].id] = parents
                else:
                    Globals.workers_factory_duty[loc_key] = {w_found[i].id: parents}
                if i == 2:
                    break


def exploreFrontier(frontier, map, parent, gc):
    newFrontier = []
    d = bc.Direction.North
    workers = []
    for f in frontier:
        for i in range(8):
            d = d.rotate_right()
            newLocation = f.add(d)
            if map.on_map(newLocation) and (newLocation.x, newLocation.y) not in parent:
                if map.is_passable_terrain_at(newLocation):
                    if gc.can_sense_location(newLocation):
                        parent[(newLocation.x, newLocation.y)] = f
                        newFrontier.append(newLocation)
                        if gc.has_unit_at_location(newLocation):
                            unit = gc.sense_unit_at_location(newLocation)
                            if unit.unit_type == bc.UnitType.Worker and unit.team == Globals.us:
                                workers.append(unit)

    return newFrontier, workers, parent


def should_replicate(gc, unit_id, d):
    if gc.round() > 750:
        return True
    workers = Globals.radar.our_num_earth_workers
    if gc.round() < 125:
        if gc.can_harvest(unit_id, d):
            limit = 14
        else:
            limit = Globals.BEGINNING_WORKER_LIMIT + Globals.radar.our_num_earth_factories*3
        if workers <= limit and workers < Globals.MAX_WORKERS:
            return True
        return False
    else:
        if workers > 6:
            return False
        return True


def should_replicate_mars(gc):
    limit = Globals.BEGINNING_WORKER_LIMIT + Globals.radar.our_num_earth_factories*3
    workers = Globals.radar.our_num_mars_workers
    if workers <= limit and workers < Globals.MAX_WORKERS:
        return True
    return False









