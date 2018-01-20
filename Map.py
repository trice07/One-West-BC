import battlecode as bc
import json



def get_enemy_map(game_map, my_team):
    """
    Takes a game_map and the users team as inputs. Returns a list where
    the enemy location is a tuple (x, y)..
    """
    enemy_map=[] #The return value
    enemies=game_map["initial_units"] #The dictionary of all units at the start of a game
    if str(my_team)=="Team.Red": #Set the team to a readable string for red
        my_team="Red"
    else: #Set the team to a readable string for blue
        my_team="Blue"
    for i in enemies: #Loops through all units and if they are not on our team, fills the enemy_map dictionary
        if i["team"]!=my_team:
            enemy_map.append((i["location"]["OnMap"]["x"], i["location"]["OnMap"]["y"]))
    return enemy_map

def get_karbonite_map(game_map):
    """
    Reutns a map of all initial karbonite values for every tile, regardless of
    passability. Takes a game map dictionary as an input.
    """
    karbonite_map={} #The return value
    karbonite=[] #A list of karbonite amounts assosciated with each tile
    for i in game_map["initial_karbonite"]: #Flattens out game_map["initial_karbonite"]
        for j in i:
            karbonite.append(j)
    karbonite=list(reversed(karbonite)) #Reverse the list so that we start at (0,0)
    width, height=get_map_size(game_map) #Gets the width and height by calling the get_map_size function
    index=0 #The index of karbonite
    for i in range(width): #Loops through all elements of passable and appends values to temps
        temp_locs=[]
        temp_karbonite=[]
        for j in range(height):
            temp_locs.append((i,j))
            temp_karbonite.append(karbonite[index])
            index+=1
        for k in range(len(temp_locs)):
            karbonite_map[temp_locs[k]]=temp_karbonite[k]
    return karbonite_map

def get_map_size(game_map):
    """
    Returns the width and height of a game map (Earth or Mars). Takes a game map dictionary as
    an input.
    """
    height=game_map["height"]
    width=game_map["width"]
    return int(width), int(height)

def get_passable_map(game_map):
    """
    Creates an array of arrays (1's and 0's) representing whether or not a space
    on the map is passable. Takes a a game map dictionary as an inputs. The map
    is a dictionary with a tuple containing (x, y) coordinates as keys and
    True/False as a value.
    """
    passable_map={} #The return value
    passable=[] #A list of True/False values assosciated with each tile
    for i in game_map["is_passable_terrain"]: #Flattens out game_map["is_passable_terrain"]
        for j in i:
            passable.append(j)
    passable=list(reversed(passable)) #Reverse the list so that we start at (0,0)
    width, height=get_map_size(game_map) #Gets the width and height by calling the get_map_size function
    index=0 #The index of passable
    for i in range(width): #Loops through all elements of passable and appends values to temps
        temp_locs=[]
        temp_passable=[]
        for j in range(height):
            temp_locs.append((i,j))
            temp_passable.append(bool(passable[index]))
            index+=1
        for k in range(len(temp_locs)):
            passable_map[temp_locs[k]]=temp_passable[k]
    return passable_map   

def has_karbonite(karbonite_map, location):
    """
    Takes in a passability map for a planet and a MapLocation object. Returns a
    an int with how much karbonite is at that space on the map.
    """
    x=location.x
    y=location.y
    return karbonite_map[(x,y)]

def initialize_earth_map(gc):
    """
    Creates a dictionary of the initial Earth map. Takes a GameController as
    input.
    """
    earth_map=json.loads(gc.starting_map(bc.Planet.Earth).to_json())
    return earth_map

def initialize_mars_map(gc):
    """
    Creates a dictionary of the initial Mars map. Takes a GameController as
    input.
    """
    mars_map=json.loads(gc.starting_map(bc.Planet.Mars).to_json())
    return mars_map

def is_passable(passable_map, location):
    """
    Takes in a passability map for a planet and a MapLocation object. Returns a
    boolean determining whether or not that space is passable.
    """
    x=location.x
    y=location.y
    return bool(passable_map[(x,y)])

# def update_enemy_map(gc, my_team, enemy_map):
#     """
#     Updates the enemy map by scanning all visible enemies from each units
#     location. Takes a GameController object, my_team, and an enemy_map as
#     inputs.
#     """
#     enemy_map=[]
#     my_team=None
#     if my_team==bc.Team.Red: #Sets the value for the enmy team
#         enemy_team=bc.Team.Blue
#     else:
#         enemy_team=bc.Team.Red
#     for unit in gc.my_units(): #Loops through all friendly units
#         if unit.location.is_on_map():
#             nearby=gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, enemy_team)
#             for other in nearby: #Loops through all units within that units vision
#                 if (other.location.map_location().x, other.location.map_location().y) not in enemy_map: #If it hasnt already been detected yet, add it to the enemy_map
#                     enemy_map.append((other.location.map_location().x, other.location.map_location().y))
#     return enemy_map

def update_karbonite_map(karbonite_map, location, karbonite_value):
    """
    Updates the amount of karbonite at a given square. Takes in a karbonite map, a
    Location object, and a karbonite value as inputs.
    """
    karbointe_map[(location.map_location().x, location.map_location.y)]=karbonite_value




    
