import battlecode as bc
import Factory
import Map
import sys
import traceback
import Units
import Research
import Rocket
import Soldier
import Worker

###Pre-Game###

gc=bc.GameController() #Creates a game controller to connect to a running game
my_team=gc.team()#Stores our teams color 
Research.fill_research_queue(gc) #Fills the research queue
factories, rockets, soldiers, workers=Units.split_units(gc) #Organizes the units by type

earth_map=Map.initialize_earth_map(gc) #Gets the earth GameMap represented as a dictionary for Earth
earth_enemy_map=Map.get_enemy_map(earth_map, my_team) #Gets the initial enemy map of Earth
earth_karbonite_map=Map.get_karbonite_map(earth_map) #Gets the initial karbonite map of Earth
earth_passable_map=Map.get_passable_map(earth_map) #Gets the passable map of Earth
earth_width, earth_width=Map.get_map_size(earth_map) #Gets the dimensions of Earth

mars_map=Map.initialize_mars_map(gc) #Gets the mars GameMap represented as a dictionary for Earth
mars_enemy_map=Map.get_enemy_map(mars_map, my_team) #Gets the initial enemy_map of Mars
mars_karbonite_map=Map.get_karbonite_map(mars_map) #Gets the initial karbonite map of Mars
mars_passable_map=Map.get_passable_map(mars_map) #Gets the passable map of Mars
mars_width, mars_height=Map.get_map_size(mars_map)

while True:
    ###Start of Turn Updates###
    
    print("Round: ", gc.round())
    print("Karbonite: ", gc.karbonite())
        
    try:
        ###Unit Controls###
        
        for unit in workers: #Workers must go first so that they have a chance to mine and replicate
            Worker.manage_worker(gc, unit)
        for unit in soldiers: #Soldiers must go before factories as well so that the unloaded soldiers can move out of the way
            Soldier.manage_soldiers(gc, unit, my_team)
        #for unit in factories:
            #Factory.factory_manager(gc, unit, factories, rockets, soldiers, workers)
        #for unit in rockets:
            #Rocket.manage_rockets(gc, unit, mars_width, mars_height, mars_passable_map)
    
        ###End of Turn Updates###

        factories, rockets, soldiers, workers=Units.update_units(gc) #Update our units at the end of a turn

    #Allows us to locate errors in the code
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    #Send the actions we have performed and wait for the next turn
    gc.next_turn()

    #Write all actions to the manager
    sys.stdout.flush()
    sys.stderr.flush()


