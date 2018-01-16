import battlecode as bc
import json

def get_enemy_center(enemy_map, planet):
    """
    Takes an enemy map as an input. Using the known enemy locations it
    calculates their center point and returns it as a MapLocation object.
    There is no guarantee that the point will be on the map and this must
    be checked. If there are no units on the planet, the center is at (0, 0)
    """
    center_x=0
    center_y=0
    count=0
    for i in enemy_map: #Loops through all x and y values in the enemy_map and sums them up
        count+=1
        center_x+=i[0]
        center_y+=i[1]
    return bc.MapLocation(planet, center_x//count, center_y//count) #Returns a MapLocation object that is at the center of the enmy forces

def get_enemy_map(game_map, my_team):
    """
    Takes a game_map and the users team as inputs. Returns a dictionary where
    the enemy location is a tuple (x, y) and the unit type is the value.
    """
    enemy_map={} #The return value
    enemies=game_map["initial_units"] #The dictionary of all units at the start of a game
    if str(my_team)=="Team.Red": #Set the team to a readable string for red
        my_team="Red"
    else: #Set the team to a readable string for blue
        my_team="Blue"
    for i in enemies: #Loops through all units and if they are not on our team, fills the enemy_map dictionary
        if i["team"]!=my_team:
            enemy_map[(i["location"]["OnMap"]["x"], i["location"]["OnMap"]["y"])]=i["unit_type"]
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

def update_karbonite_map(karbonite_map, location, karbonite_value):
    """
    Updates the amount of karbonite at a given square. Takes in a karbonite map, a
    Location object, and a karbonite value as inputs.
    """
    karbointe_map[(location.map_location().x, location.map_location.y)]=karbonite_value


    
