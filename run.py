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
from Radar import Radar

# Pre-Game #

gc = bc.GameController() #Creates a game controller to connect to a running game
Globals.us = gc.team()#Stores our teams color
if Globals.us == bc.Team.Red: #Assigns a value to the enemy team
    Globals.them = bc.Team.Blue
else:
    Globals.them = bc.Team.Red
Research.fill_research_queue(gc)  # Fills the research queue

# earth_map=Map.initialize_earth_map(gc) #Gets the earth GameMap represented as a dictionary for Earth
# earth_enemy_map=Map.get_enemy_map(earth_map, Globals.us) #Gets the initial enemy map of Earth
# earth_width, earth_width=Map.get_map_size(earth_map) #Gets the dimensions of Earth
#
# mars_map=Map.initialize_mars_map(gc) #Gets the mars GameMap represented as a dictionary for Earth
# mars_enemy_map=Map.get_enemy_map(mars_map, Globals.us) #Gets the initial enemy_map of Mars
# mars_width, mars_height=Map.get_map_size(mars_map)

Globals.radar = Radar(gc.starting_map(bc.Planet.Earth), gc.starting_map(bc.Planet.Mars))
Globals.earth_enemy_center = Globals.radar.get_enemy_center(bc.Planet.Earth)  # The center of starting enemy units on Earth


while True:
    # Start of Turn Updates #
    
    # print("Round: ", gc.round())
    # print("Karbonite: ", gc.karbonite())
        
    try:
        # Globals.radar.update_mars_karb(gc)
        # Unit Controls #
        if gc.round() % 25 == 0:
            Navigation.BFS(gc.starting_map(bc.Planet.Earth), Globals.radar.get_enemy_center(bc.Planet.Earth))
        for unit in gc.my_units():
            if Units.try_go_to_rocket(gc, unit):
                continue
            Globals.radar.update_location(unit)
            if unit.location.is_on_map():
                if unit.unit_type == bc.UnitType.Worker:
                    Worker.manage_worker(gc, unit)
                elif unit.unit_type == bc.UnitType.Rocket:
                    Rocket.manage_rockets(gc, unit)
                elif unit.unit_type == bc.UnitType.Healer:
                    Healer.manage_healers(gc, unit)
                elif unit.unit_type == bc.UnitType.Knight:
                    pass
                    # Knight.manage_knights(gc, unit, Globals.earth_enemy_center, earth_enemy_map, eneGlobals.us)
                elif unit.unit_type == bc.UnitType.Mage:
                    pass
                    # Mage.manage_mages(gc, unit, Globals.earth_enemy_center, earth_enemy_map, Globals.us)
                elif unit.unit_type == bc.UnitType.Ranger:
                    Ranger.turn(gc, unit)
                elif unit.unit_type == bc.UnitType.Factory:
                    Factory.factory_manager(gc, unit)
        Globals.radar.remove_dead_enemies()

    # Allows us to locate errors in the code
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # Send the actions we have performed and wait for the next turn
    Globals.radar.clear_being_shot_at_cache(bc.Planet.Earth)
    Globals.radar.clear_being_shot_at_cache(bc.Planet.Mars)
    gc.next_turn()

    # Write all actions to the manager
    sys.stdout.flush()
    sys.stderr.flush()


