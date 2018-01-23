import battlecode as bc

import Globals
import Navigation

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
        self.enemy_earth_x_sum = 0
        self.enemy_earth_y_sum = 0

        self.mars_map = {}
        self.mars_karbonite_locations = []
        self.our_mars_locations = {}
        self.mars_enemy_locations = {}
        self.being_shot_at_mars = []
        self.enemy_mars_x_sum = 0
        self.enemy_mars_y_sum = 0

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

        self.current_units = {}
        self.previous_units = {}

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
                self.previous_units[unit.id] = unit
            self.update_unit_counts_earth(unit, "+")

        # Initialize Mars Map
        for i in range(mars.width):
            for j in range(mars.height):
                ml = bc.MapLocation(mars.planet, i, j)
                to_add = Radar.get_init_type(ml, mars)
                coords = Radar.get_coordinates(ml)
                self.mars_map[coords] = to_add

    def update_unit_counts_earth(self, unit, command):
        t = unit.unit_type
        l = unit.location.map_location()
        x = l.x
        y = l.y
        if command == "+":
            if unit.team == Globals.them:
                self.enemy_earth_x_sum += x
                self.enemy_earth_y_sum += y
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
        elif command == "-":
            if unit.team == Globals.them:
                self.enemy_earth_x_sum -= x
                self.enemy_earth_y_sum -= y
                if t == bc.UnitType.Ranger:
                    self.their_num_earth_rangers -= 1
                elif t == bc.UnitType.Factory:
                    self.their_num_earth_factories -= 1
                elif t == bc.UnitType.Rocket:
                    self.their_num_earth_rockets -= 1
                elif t == bc.UnitType.Mage:
                    self.their_num_earth_mages -= 1
                elif t == bc.UnitType.Worker:
                    self.their_num_earth_workers -= 1
                elif t == bc.UnitType.Knight:
                    self.their_num_earth_knights -= 1
                elif t == bc.UnitType.Healer:
                    self.their_num_earth_healers -= 1
            else:
                if t == bc.UnitType.Ranger:
                    self.our_num_earth_rangers -= 1
                elif t == bc.UnitType.Factory:
                    self.our_num_earth_factories -= 1
                elif t == bc.UnitType.Rocket:
                    self.our_num_earth_rockets -= 1
                elif t == bc.UnitType.Mage:
                    self.our_num_earth_mages -= 1
                elif t == bc.UnitType.Worker:
                    self.our_num_earth_workers -= 1
                elif t == bc.UnitType.Knight:
                    self.our_num_earth_knights -= 1
                elif t == bc.UnitType.Healer:
                    self.our_num_earth_healers -= 1

    def update_unit_counts_mars(self, unit, command):
        t = unit.unit_type
        l = unit.location.map_location()
        x = l.x
        y = l.y
        if command == "+":
            if unit.team == Globals.them:
                self.enemy_mars_x_sum += x
                self.enemy_mars_y_sum += y
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
        elif command == "-":
            if unit.team == Globals.them:
                self.enemy_mars_x_sum -= x
                self.enemy_mars_y_sum -= y
                if t == bc.UnitType.Ranger:
                    self.their_num_earth_rangers -= 1
                elif t == bc.UnitType.Factory:
                    self.their_num_earth_factories -= 1
                elif t == bc.UnitType.Rocket:
                    self.their_num_earth_rockets -= 1
                elif t == bc.UnitType.Mage:
                    self.their_num_earth_mages -= 1
                elif t == bc.UnitType.Worker:
                    self.their_num_earth_workers -= 1
                elif t == bc.UnitType.Knight:
                    self.their_num_earth_knights -= 1
                elif t == bc.UnitType.Healer:
                    self.their_num_earth_healers -= 1
            else:
                if t == bc.UnitType.Ranger:
                    self.our_num_earth_rangers -= 1
                elif t == bc.UnitType.Factory:
                    self.our_num_earth_factories -= 1
                elif t == bc.UnitType.Rocket:
                    self.our_num_earth_rockets -= 1
                elif t == bc.UnitType.Mage:
                    self.our_num_earth_mages -= 1
                elif t == bc.UnitType.Worker:
                    self.our_num_earth_workers -= 1
                elif t == bc.UnitType.Knight:
                    self.our_num_earth_knights -= 1
                elif t == bc.UnitType.Healer:
                    self.our_num_earth_healers -= 1

    def update_radar(self, gc, unit):
        vecunit = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.vision_range, Globals.them)
        for enemy in vecunit:
            self.update_enemy_cache(enemy)
        return vecunit

    def update_location(self, unit):
        if unit.location.is_on_planet(bc.Planet.Earth):
            cache = self.our_earth_locations
            planet = bc.Planet.Earth
        elif unit.location.is_on_planet(bc.Planet.Mars):
            cache = self.our_mars_locations
            planet = bc.Planet.Mars
        else:
            return
        if unit.id not in cache:
            if planet == bc.Planet.Earth:
                self.update_unit_counts_earth(unit, "+")
            else:
                self.update_unit_counts_mars(unit, "+")
            # if unit.unit_type == bc.UnitType.Factory:
            #     Navigation.disperse(gc, unit)
            #     Navigation.straightToEnemy(gc, unit)
            # if unit.unit_type == bc.UnitType.Rocket and unit.location.is_on_planet(bc.Planet.Mars):
            #     Navigation.disperse(gc, unit)
            #     print(Globals.paths_to_disperse_mars)
        cache[unit.id] = unit
        self.current_units[unit.id] = unit
        if unit.id in self.previous_units:
            del self.previous_units[unit.id]

    def remove_dead_enemies(self):
        for unit_id in self.previous_units:
            unit = self.previous_units[unit_id]
            if unit.location.is_on_planet(bc.Planet.Earth):
                self.update_unit_counts_earth(unit, "-")
                del self.our_earth_locations[unit_id]
            else:
                self.update_unit_counts_mars(unit, "-")
                del self.our_mars_locations[unit_id]
        self.previous_units = self.current_units
        self.current_units = {}

    def update_enemy_cache(self, enemy):
        if enemy.location.is_on_planet(bc.Planet.Earth):
            cache = self.earth_enemy_locations
            planet = bc.Planet.Earth
        elif enemy.location.is_on_planet(bc.Planet.Mars):
            cache = self.mars_enemy_locations
            planet = bc.Planet.Mars
        else:
            return
        if enemy.id not in cache:
            if planet == bc.Planet.Earth:
                self.update_unit_counts_earth(enemy, "+")
            else:
                self.update_unit_counts_mars(enemy, "+")
        cache[enemy.id] = enemy

    def clear_being_shot_at_cache(self, planet):
        if planet == bc.Planet.Earth:
            self.being_shot_at_earth = []
        elif planet == bc.Planet.Mars:
            self.being_shot_at_mars = []
        return


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
            center_x = self.enemy_earth_x_sum
            center_y = self.enemy_earth_y_sum
            count = len(self.earth_enemy_locations)
        elif planet == bc.Planet.Mars:
            cache = self.mars_enemy_locations
            center_x = self.enemy_mars_x_sum
            center_y = self.enemy_mars_y_sum
            count = len(self.mars_enemy_locations)
        else:
            return None
        if len(cache) == 0:
            return None
        return bc.MapLocation(planet, center_x//count, center_y//count)  # Returns a MapLocation object that is at the center of the e forces

    def delete_enemy_from_radar(self, enemy):
        del Globals.radar.earth_enemy_locations[enemy.id]
        if enemy.location.is_on_planet(bc.Planet.Earth):
            self.update_unit_counts_earth(enemy, "-")
        elif enemy.location.is_on_planet(bc.Planet.Mars):
            self.update_unit_counts_mars(enemy, "-")

