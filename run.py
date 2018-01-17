import battlecode as bc
import Factory
import Healer
import Knight
import Mage
import Map
import sys
import traceback
import Ranger
import Research
import Rocket
import Worker
import Globals
from Radar import Radar

###Pre-Game###

gc=bc.GameController() #Creates a game controller to connect to a running game
my_team=gc.team()#Stores our teams color 
Research.fill_research_queue(gc) #Fills the research queue

earth_map=Map.initialize_earth_map(gc) #Gets the earth GameMap represented as a dictionary for Earth
earth_enemy_map=Map.get_enemy_map(earth_map, my_team) #Gets the initial enemy map of Earth
earth_karbonite_map=Map.get_karbonite_map(earth_map) #Gets the initial karbonite map of Earth
earth_passable_map=Map.get_passable_map(earth_map) #Gets the passable map of Earth
earth_width, earth_width=Map.get_map_size(earth_map) #Gets the dimensions of Earth
earth_enemy_center=Map.get_enemy_center(earth_enemy_map, bc.Planet.Earth) #The center of starting enemy units on Earth
mars_map=Map.initialize_mars_map(gc) #Gets the mars GameMap represented as a dictionary for Earth
mars_enemy_map=Map.get_enemy_map(mars_map, my_team) #Gets the initial enemy_map of Mars
mars_karbonite_map=Map.get_karbonite_map(mars_map) #Gets the initial karbonite map of Mars
mars_passable_map=Map.get_passable_map(mars_map) #Gets the passable map of Mars
mars_width, mars_height=Map.get_map_size(mars_map)

Globals.earth_enemy_center = earth_enemy_center
Globals.radar = Radar(gc.starting_map(bc.Planet.Earth), gc.starting_map(bc.Planet.Mars))


while True:
    ###Start of Turn Updates###
    
    print("Round: ", gc.round())
    print("Karbonite: ", gc.karbonite())
        
    try:
        ###Unit Controls###
        for unit in gc.my_units():
            if unit.location.is_on_map():
                if unit.unit_type==bc.UnitType.Worker:
                    Worker.manage_worker(gc, unit)
                elif unit.unit_type==bc.UnitType.Healer:
                    Healer.manage_healers(gc, unit, my_team)
                elif unit.unit_type==bc.UnitType.Knight:
                    Knight.manage_knights(gc, unit, my_team, earth_enemy_center)                   
                elif unit.unit_type==bc.UnitType.Mage:
                    Mage.manage_mages(gc, unit, my_team, earth_enemy_center)
                elif unit.unit_type==bc.UnitType.Ranger:
                    Ranger.turn(gc, unit)
                elif unit.unit_type==bc.UnitType.Factory:
                    Factory.factory_manager(gc, unit)
                #elif unit.unit_type==bc.UnitType.Rocket:
                    #Rocket.manage_rockets(gc, unit, mars_width, mars_height, mars_passable_map)
    
    #Allows us to locate errors in the code
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    #Send the actions we have performed and wait for the next turn
    gc.next_turn()

    #Write all actions to the manager
    sys.stdout.flush()
    sys.stderr.flush()


