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
        self.earth_karbonite_locations = {}
        self.our_earth_locations = {}
        self.earth_enemy_locations = {}
        self.being_shot_at_earth = {}
        self.enemy_earth_x_sum = 0
        self.enemy_earth_y_sum = 0

        self.mars_map = {}
        self.mars_karbonite_locations = {}
        self.our_mars_locations = {}
        self.mars_enemy_locations = {}
        self.being_shot_at_mars = {}
        self.enemy_mars_x_sum = 0
        self.enemy_mars_y_sum = 0
        self.poss_landing_locations = []

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
        self.enemies_killed_this_turn = {}

        self.enemy_center_found = -1
        self.enemy_center = None

        # Initialize Earth Map
        for i in range(earth.width):
            for j in range(earth.height):
                ml = bc.MapLocation(earth.planet, i, j)
                to_add = Radar.get_init_type(ml, earth)
                if to_add["karb"] != 0:
                    self.earth_karbonite_locations[(ml.x, ml.y)] = to_add["karb"]
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
                if to_add["passable"]:
                    self.poss_landing_locations.append(ml)
                if to_add["karb"] != 0:
                    self.mars_karbonite_locations[(ml.x, ml.y)] = to_add["karb"]
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

    def update_radar(self, gc, unit, r=None):
        if r is None:
            r = unit.vision_range
        vecunit = gc.sense_nearby_units_by_team(unit.location.map_location(), r, Globals.them)
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
        cache[unit.id] = unit
        self.current_units[unit.id] = unit
        if unit.id in self.previous_units:
            del self.previous_units[unit.id]

    def remove_dead_units(self):
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
            x_sum = self.enemy_earth_x_sum
            y_sum = self.enemy_earth_y_sum
        elif enemy.location.is_on_planet(bc.Planet.Mars):
            cache = self.mars_enemy_locations
            planet = bc.Planet.Mars
            x_sum = self.enemy_mars_x_sum
            y_sum = self.enemy_mars_y_sum
        else:
            return
        if enemy.id not in cache:
            if planet == bc.Planet.Earth:
                self.update_unit_counts_earth(enemy, "+")
            else:
                self.update_unit_counts_mars(enemy, "+")
        # else:
        #     x, y = self.get_coordinates(cache[enemy.id].location)
        #     newx, newy = self.get_coordinates(enemy.location)
        #     x_sum -= x
        #     y_sum -= y
        #     x_sum += newx
        #     y_sum += newy
        cache[enemy.id] = enemy

    def clear_being_shot_at_cache(self, planet):
        if planet == bc.Planet.Earth:
            self.being_shot_at_earth = {}
        elif planet == bc.Planet.Mars:
            self.being_shot_at_mars = {}
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

    def update_karb_amount(self, gc, location, asteroid=False):
        coords = self.get_coordinates(location)
        if location.planet == bc.Planet.Earth:
            amount = gc.karbonite_at(location)
            self.earth_map[coords]["karb"] = amount
            if amount == 0:
                self.earth_karbonite_locations[(location.x, location.y)] = 0
        elif location.planet == bc.Planet.Mars:
            if isinstance(asteroid, int):
                self.mars_map[coords]["karb"] = asteroid
            else:
                amount = gc.karbonite_at(location)
                self.mars_map[coords]["karb"] = amount
                if amount == 0:
                    self.mars_karbonite_locations[(location.x, location.y)] = 0
                elif location not in self.mars_karbonite_locations:
                    self.mars_karbonite_locations[(location.x, location.y)] = amount

    def get_enemy_center(self, planet):
        """
        Takes an enemy map as an input. Using the known enemy locations it
        calculates their center point and returns it as a MapLocation object.
        There is no guarantee that the point will be on the map and this must
        be checked. If there are no units on the planet, the center is at (0, 0)
        """

        if planet == bc.Planet.Earth:
            cache = self.earth_enemy_locations
            # center_x = self.enemy_earth_x_sum
            # center_y = self.enemy_earth_y_sum
            count = len(self.earth_enemy_locations)
            if count == 0:
                return bc.MapLocation(bc.Planet.Earth, Globals.earth_width//2, Globals.earth_height//2)
        elif planet == bc.Planet.Mars:
            cache = self.mars_enemy_locations
            # center_x = self.enemy_mars_x_sum
            # center_y = self.enemy_mars_y_sum
            count = len(self.mars_enemy_locations)
            if count == 0:
                return bc.MapLocation(bc.Planet.Mars, Globals.mars_width//2, Globals.mars_height//2)
        else:
            return None
        if len(cache) == self.enemy_center_found:
            return self.enemy_center
        center_x = 0
        center_y = 0
        for e in cache:
            center_x += cache[e].location.map_location().x
            center_y += cache[e].location.map_location().y
        ec = bc.MapLocation(planet, center_x//count, center_y//count)
        self.enemy_center = ec
        self.enemy_center_found = len(cache)
        return ec

    def delete_enemy_from_radar(self, enemy):
        if enemy.location.is_on_planet(bc.Planet.Earth):
            self.update_unit_counts_earth(enemy, "-")
            del self.earth_enemy_locations[enemy.id]
        elif enemy.location.is_on_planet(bc.Planet.Mars):
            self.update_unit_counts_mars(enemy, "-")
            del self.mars_enemy_locations[enemy.id]

    def check_if_enemies_gone(self, gc, unit):
        if gc.round() > 250:
            ml = unit.location.map_location()
            if ml == self.get_enemy_center(ml.planet) and len(self.earth_enemy_locations) == 0:
                return True
            elif len(self.mars_enemy_locations) == 0:
                return True
        return False
