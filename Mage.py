import battlecode as bc
import random
import Ranger
import Globals
import Navigation
import Units

directions=list(bc.Direction) #Stores all directions as a list
random.seed(1) #Random seeding for testing. Will be removed
arrived=[] #List of units who got close to the objective

def manage_mages(gc, unit):
    """
    Runs all of the mages. Takes in a GameController object, a unit,
    the starting center of enemy activity, an enemy_map, and the enemy
    team as inputs.
    """
    enemies = Units.shoot_at_best_target(gc, unit)
    loc = unit.location.map_location()
    path = Globals.pathToEnemy if loc.planet == bc.Planet.Earth else Globals.pathToEnemyMars
    if isinstance(enemies, bc.Unit):
        return
    else:
        if Ranger.ranger_retreat(unit, enemies):
            if gc.is_move_ready(unit.id):
                retreated = Navigation.retreatFromKnownEnemy(gc, unit, Globals.radar.get_enemy_center(loc.planet))
                if not retreated:
                    if gc.is_blink_ready(unit.id):
                        go_blink(gc, unit, loc)
                    else:
                        if gc.is_move_ready(unit.id):
                            Navigation.path_with_bfs(gc, unit, path)
        else:
            if gc.is_blink_ready(unit.id):
                go_blink(gc, unit, loc)
            else:
                if gc.is_move_ready(unit.id):
                    Navigation.path_with_bfs(gc, unit, path)


def go_blink(gc, unit, loc):
    enemycenter = Globals.radar.get_enemy_center(loc.planet)
    d = bc.Direction.North
    for i in range(8):
        if check_blink_location(gc, unit, enemycenter):
            return
        enemycenter = enemycenter.add(d)


def check_blink_location(gc, unit, destination):
    if gc.can_blink(unit.id, destination):
        nearby = gc.sense_nearby_units_by_team(destination, 2, Globals.them)
        if len(nearby) > 0:
            gc.blink(unit.id, destination)
            return True
    return False

        
        

