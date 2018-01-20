import battlecode as bc
import Globals


class Radar:
    def __init__(self, earth, mars):
        """
        Initialize Radar
        :param earth: PlanetMap
        :param mars: PlanetMap
        """
        self.earth_map = {}
        self.earth_karbonite_locations = []
        self.our_earth_locations = {}
        self.earth_enemy_locations = {}
        self.being_shot_at_earth = []

        self.mars_map = {}
        self.mars_karbonite_locations = []
        self.our_mars_locations = {}
        self.mars_enemy_locations = {}
        self.being_shot_at_mars = []

        self.our_num_earth_workers = 0
        self.our_num_earth_knights = 0
        self.our_num_earth_mages = 0
        self.our_num_earth_rangers = 0
        self.our_num_earth_healers = 0
        self.our_num_earth_factories = 0
        self.our_num_earth_rockets = 0
        self.their_num_earth_workers = 0
        self.their_num_earth_knights = 0
        self.their_num_earth_mages = 0
        self.their_num_earth_rangers = 0
        self.their_num_earth_healers = 0
        self.their_num_earth_factories = 0
        self.their_num_earth_rockets = 0

        self.our_num_mars_workers = 0
        self.our_num_mars_knights = 0
        self.our_num_mars_mages = 0
        self.our_num_mars_rangers = 0
        self.our_num_mars_healers = 0
        self.our_num_mars_rockets = 0
        self.their_num_mars_workers = 0
        self.their_num_mars_knights = 0
        self.their_num_mars_mages = 0
        self.their_num_mars_rangers = 0
        self.their_num_mars_healers = 0
        self.their_num_mars_rockets = 0

        # Initialize Earth Map
        for i in range(earth.width):
            for j in range(earth.height):
                ml = bc.MapLocation(earth.planet, i, j)
                to_add = Radar.get_init_type(ml, earth)
                if to_add["karb"] != 0:
                    self.earth_karbonite_locations.append(ml)
                coords = Radar.get_coordinates(ml)
                self.earth_map[coords] = to_add

        # Initialize unit locations
        for unit in earth.initial_units:
            location = Radar.get_coordinates(unit.location)
            self.earth_map[location]["passable"] = False
            if unit.team == Globals.them:
                self.earth_enemy_locations[unit.id] = unit
            else:
                self.our_earth_locations[unit.id] = unit
            self.update_unit_counts_earth(unit)

        # Initialize Mars Map
        for i in range(mars.width):
            for j in range(mars.height):
                ml = bc.MapLocation(mars.planet, i, j)
                to_add = Radar.get_init_type(ml, mars)
                coords = Radar.get_coordinates(ml)
                self.mars_map[coords] = to_add

    def update_unit_counts_earth(self, unit):
        t = unit.unit_type
        if unit.team == Globals.them:
            if t == bc.UnitType.Ranger:
                self.their_num_earth_rangers += 1
            elif t == bc.UnitType.Factory:
                self.their_num_earth_factories += 1
            elif t == bc.UnitType.Rocket:
                self.their_num_earth_rockets += 1
            elif t == bc.UnitType.Mage:
                self.their_num_earth_mages += 1
            elif t == bc.UnitType.Worker:
                self.their_num_earth_workers += 1
            elif t == bc.UnitType.Knight:
                self.their_num_earth_knights += 1
            elif t == bc.UnitType.Healer:
                self.their_num_earth_healers += 1
        else:
            if t == bc.UnitType.Ranger:
                self.our_num_earth_rangers += 1
            elif t == bc.UnitType.Factory:
                self.our_num_earth_factories += 1
            elif t == bc.UnitType.Rocket:
                self.our_num_earth_rockets += 1
            elif t == bc.UnitType.Mage:
                self.our_num_earth_mages += 1
            elif t == bc.UnitType.Worker:
                self.our_num_earth_workers += 1
            elif t == bc.UnitType.Knight:
                self.our_num_earth_knights += 1
            elif t == bc.UnitType.Healer:
                self.our_num_earth_healers += 1

    def update_unit_counts_mars(self, unit):
        t = unit.unit_type
        if unit.team == Globals.them:
            if t == bc.UnitType.Ranger:
                self.their_num_mars_rangers += 1
            elif t == bc.UnitType.Rocket:
                self.their_num_mars_rockets += 1
            elif t == bc.UnitType.Mage:
                self.their_num_mars_mages += 1
            elif t == bc.UnitType.Worker:
                self.their_num_mars_workers += 1
            elif t == bc.UnitType.Knight:
                self.their_num_mars_knights += 1
            elif t == bc.UnitType.Healer:
                self.their_num_mars_healers += 1
        else:
            if t == bc.UnitType.Ranger:
                self.our_num_mars_rangers += 1
            elif t == bc.UnitType.Rocket:
                self.our_num_mars_rockets += 1
            elif t == bc.UnitType.Mage:
                self.our_num_mars_mages += 1
            elif t == bc.UnitType.Worker:
                self.our_num_mars_workers += 1
            elif t == bc.UnitType.Knight:
                self.our_num_mars_knights += 1
            elif t == bc.UnitType.Healer:
                self.our_num_mars_healers += 1

    def update_radar(self, gc, unit):
        vecunit = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, Globals.them)
        for enemy in vecunit:
            self.update_enemy_cache(enemy)
        return vecunit

    def update_location(self, unit):
        if unit.location.is_on_planet(bc.Planet.Earth):
            cache = self.our_earth_locations
        elif unit.location.is_on_planet(bc.Planet.Mars):
            cache = self.our_mars_locations
        else:
            return
        cache[unit.id] = unit

    def update_enemy_cache(self, enemy):
        if enemy.location.is_on_planet(bc.Planet.Earth):
            cache = self.earth_enemy_locations
        elif enemy.location.is_on_planet(bc.Planet.Mars):
            cache = self.mars_enemy_locations
        else:
            return
        cache[enemy.id] = enemy

    def clear_being_shot_at_cache(self, planet):
        if planet == bc.Planet.Earth:
            self.being_shot_at_earth = []
        elif planet == bc.Planet.Mars:
            self.being_shot_at_mars = []
        return

    # def find_closest_target(self, unit):
    #     best = None
    #     target = None
    #     me = unit.location.map_location()
    #     for enemy in self.enemy_locations:
    #         them = self.enemy_locations[enemy].location.maplocation()
    #         distance = me.distance_squared_to(them)
    #         if best is None or distance < best:
    #             best = distance
    #             target = them
    #     return target
    #
    # def find_closest_attackable_target(self, unit):
    #     best = None
    #     target = None
    #     me = unit.location.map_location()
    #     for enemy in self.enemy_locations:
    #         them = self.enemy_locations[enemy].location.maplocation()
    #         distance = me.distance_squared_to(them)
    #         range = unit.attack_range()
    #         if distance < range:
    #             if best == None or distance < best:
    #                 best = distance
    #                 target = them
    #     return target

    # def update_closest_target(self, unit, prev):
    #     me = unit.location.map_location()
    #     best = me.distance_squared_to(prev)
    #     target = prev
    #     ranger_range = 0
    #     if unit.type == bc.UnitType.Ranger:
    #         ranger_range = unit.ranger_cannot_attack_range()
    #     for enemy in self.new_enemy_updates:
    #         distance = me.distance_squared_to(enemy)
    #         range = unit.attack_range()
    #         if ranger_range <= distance < range:
    #             if best is None or distance < best:
    #                 best = distance
    #                 target = enemy
    #     return target

    @staticmethod
    def get_init_type(ml, planet):
        return {
            "karb": planet.initial_karbonite_at(ml),
            "passable": planet.is_passable_terrain_at(ml),
        }

    @staticmethod
    def get_coordinates(location):
        if isinstance(location, bc.Location):
            location = location.map_location()
        return location.x, location.y

    def get_carb_amount(self, planet, location):
        if isinstance(location, bc.Location):
            location = location.map_location()
        if isinstance(location, bc.MapLocation):
            x = location.x
            y = location.y
            location = (x, y)
        if planet == bc.Planet.Mars:
            return self.mars_map[location]["karb"]
        if planet == bc.Planet.Earth:
            return self.earth_map[location]["karb"]
        else:
            print("Planet type not specified, make sure planet is a Planet object.")
            raise TypeError

    def get_unit_at_location(self, planet, location):
        if isinstance(location, bc.Location):
            location = location.map_location()
        if isinstance(location, bc.MapLocation):
            x = location.x
            y = location.y
            location = (x, y)
        if planet == bc.Planet.Mars:
            return self.mars_map[location]["unit"]
        if planet == bc.Planet.Earth:
            return self.earth_map[location]["unit"]
        else:
            print("Planet type not specified, make sure planet is a Planet object.")
            raise TypeError

    def is_terrain_passable(self, planet, location):
        if isinstance(location, bc.Location):
            location = location.map_location()
        if isinstance(location, bc.MapLocation):
            x = location.x
            y = location.y
            location = (x, y)
        if planet == bc.Planet.Mars:
            return self.mars_map[location]["passable"]
        if planet == bc.Planet.Earth:
            return self.earth_map[location]["passable"]
        else:
            print("Planet type not specified, make sure planet is a Planet object.")
            return

    def update_karb_amount(self, location, gc):
        amount = gc.karbonite_at(location)
        coords = self.get_coordinates(location)
        if location.planet == bc.Planet.Earth:
            self.earth_map[coords]["karb"] = amount
            if amount == 0:
                self.earth_karbonite_locations.remove(location)
        elif location.planet == bc.Planet.Mars:
            self.mars_map[coords]["karb"] = amount
            if amount == 0:
                self.mars_karbonite_locations.remove(location)
            elif location not in self.mars_karbonite_locations:
                self.mars_karbonite_locations.append(location)

    def get_enemy_center(self, planet):
        """
        Takes an enemy map as an input. Using the known enemy locations it
        calculates their center point and returns it as a MapLocation object.
        There is no guarantee that the point will be on the map and this must
        be checked. If there are no units on the planet, the center is at (0, 0)
        """
        if planet == bc.Planet.Earth:
            cache = self.earth_enemy_locations
        elif planet == bc.Planet.Mars:
            cache = self.mars_enemy_locations
        else:
            return None
        if len(cache) == 0:
            return None
        center_x = 0
        center_y = 0
        count = 0
        for i in cache:  # Loops through all x and y values in the enemy_map and sums them up
            count += 1
            center_x += cache[i].location.map_location().y
            center_y += cache[i].location.map_location().y
        return bc.MapLocation(planet, center_x//count, center_y//count)  # Returns a MapLocation object that is at the center of the e forces
