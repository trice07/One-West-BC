import battlecode as bc
import sys
import traceback
import Units
import Factory
import Globals
import Healer
import Ranger
import Research
import Rocket
import Worker
import Mage
import Knight
from Radar import Radar
import Navigation
import time
import MapStrat

# Pre-Game #

gc = bc.GameController() #Creates a game controller to connect to a running game
Globals.us = gc.team()#Stores our teams color
if Globals.us == bc.Team.Red: #Assigns a value to the enemy team
    Globals.them = bc.Team.Blue
else:
    Globals.them = bc.Team.Red
earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)
Research.fill_research_queue(gc)  # Fills the research queue
Globals.radar = Radar(gc.starting_map(bc.Planet.Earth), gc.starting_map(bc.Planet.Mars))
Globals.earth_enemy_center = Globals.radar.get_enemy_center(bc.Planet.Earth)  # The center of starting enemy units on Earth
Globals.asteroid_pattern = gc.asteroid_pattern()
Globals.pathsToKarb = MapStrat.get_paths_to_karb(earth_map)
Globals.pathToEnemy = Navigation.BFS(earth_map, Globals.radar.get_enemy_center(bc.Planet.Earth), gc)
Globals.pathToEnemyMars = Navigation.BFS(mars_map, Globals.radar.get_enemy_center(bc.Planet.Mars), gc)
Globals.INITIAL_DISTANCE = MapStrat.initial_distance()
while True:
    # Start of Turn Updates #
    
    print("Round: ", gc.round())
    # print("Karbonite: ", gc.karbonite())
        
    try:
        # Globals.radar.update_mars_karb(gc)
        # Unit Controls #
        round = gc.round()
        if round % 10 == 0:
            if Globals.radar.our_num_mars_rockets > 0:
                Globals.updatePathMars = Navigation.BFS(mars_map, Globals.radar.get_enemy_center(bc.Planet.Mars), gc)
            if Globals.radar.our_num_earth_rangers > 0:
                Globals.updatePath = Navigation.BFS(earth_map, Globals.radar.get_enemy_center(bc.Planet.Earth), gc)
            # print(Globals.pathToEnemy)
        asteroid = None
        if (round > 250 and Globals.radar.our_num_earth_rockets < 1) or round > 600:
            Globals.factory_hold = True
        else:
            Globals.factory_hold = False

        if Globals.asteroid_pattern.has_asteroid(round):
            asteroid = Globals.asteroid_pattern.asteroid(round)
        if asteroid is not None:
            Globals.radar.update_karb_amount(gc, asteroid.location, asteroid.karbonite)
        for unit in gc.my_units():
            Globals.radar.update_location(unit)
            if Units.try_go_to_rocket(gc, unit):
                continue
            if unit.location.is_on_map():
                if Globals.radar.check_if_enemies_gone(gc, unit):
                    Globals.everyone_to_mars = True
                    print("GET THE FUCK TO MARS!")
                if unit.location.map_location().planet == bc.Planet.Mars and Globals.on_mars is False:
                    Globals.on_mars = True
                    Navigation.BFS(gc.starting_map(bc.Planet.Mars), Globals.radar.get_enemy_center(bc.Planet.Mars), gc)
                if unit.unit_type == bc.UnitType.Worker:
                    s = time.time()
                    Worker.manage_worker(gc, unit)
                    Globals.wtime += (time.time() - s)
                elif unit.unit_type == bc.UnitType.Rocket:
                    Rocket.manage_rockets(gc, unit)
                elif unit.unit_type == bc.UnitType.Healer:
                    Healer.manage_healers(gc, unit)
                elif unit.unit_type == bc.UnitType.Knight:
                    Knight.turn(gc, unit)
                    # Knight.manage_knights(gc, unit, Globals.earth_enemy_center, earth_enemy_map, eneGlobals.us)
                elif unit.unit_type == bc.UnitType.Mage:
                    Mage.manage_mages(gc, unit)
                    # Mage.manage_mages(gc, unit, Globals.earth_enemy_center, earth_enemy_map, Globals.us)
                elif unit.unit_type == bc.UnitType.Ranger:
                    s = time.time()
                    Ranger.turn(gc, unit)
                    Globals.rtime += (time.time() - s)
                elif unit.unit_type == bc.UnitType.Factory:
                    Factory.factory_manager(gc, unit)
        print("Workers: ", Globals.wtime, "Rangers: ", Globals.rtime, "Find Karb: ", Globals.ftime)
        Globals.radar.remove_dead_units()
        Globals.radar.clear_being_shot_at_cache(bc.Planet.Earth)
        Globals.radar.clear_being_shot_at_cache(bc.Planet.Mars)
        Globals.radar.enemies_killed_this_turn = {}
        Globals.radar.enemy_center = None
        Globals.radar.enemy_center_found = -1
        # Globals.income = gc.karbonite() - Globals.prev_karb_amount
        # Globals.prev_karb_amount = gc.karbonite()
        print("----------------")
    # Allows us to locate errors in the code
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # Send the actions we have performed and wait for the next turn
    gc.next_turn()

    # Write all actions to the manager
    sys.stdout.flush()
    sys.stderr.flush()


