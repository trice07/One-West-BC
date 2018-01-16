import battlecode as bc


class Radar:
    def __init__(self, earth, mars):
        mars_map = {}
        earth_map = {}
        self.earth_karboniteLocations = []
        self.mars_karboniteLocations = []
        units = earth.initial_units
        for i in range(earth.width):
            for j in range(earth.height):
                ml = bc.MapLocation(earth.planet, i, j)
                toadd = Radar.get_init_type(ml, earth)
                if toadd["karb"] != 0:
                    self.karboniteLocations.append(ml)
                coords = Radar.get_coordinates(ml)
                earth_map[coords] = toadd
        for unit in units:
            location = unit.location.map_location()
            # earth_map[location]["unit"] = unit
            # earth_map[location]["foe"] = False
            earth_map[location]["passable"] = False
        for i in range(mars.width):
            for j in range(mars.height):
                ml = bc.MapLocation(mars.planet, i, j)
                toadd = Radar.get_init_type(ml, mars)
                coords = Radar.get_coordinates(ml)
                mars_map[coords] = toadd
        self.earth_map = earth_map
        self.mars_map = mars_map
        self.enemy_locations = {}
        self.new_enemy_updates = {}


    def update_radar(self, gc, unit):
        if unit.team == bc.Team.Red:
            team = bc.Team.Blue
        else:
            team = bc.Team.Red
        vecunit = gc.sense_nearby_units_by_team(unit.location, unit.vision_range, team)
        for unit in vecunit:
            if unit.id not in self.enemy_locations:
                self.enemy_locations[unit.id] = {unit}
                self.new_enemy_updates[unit.location.map_location()] = unit
            elif self.enemy_locations[unit.id].location != unit.location:
                self.enemy_locations[unit.id] = unit
                self.new_enemy_updates[unit.location.map_location()] = unit
        return vecunit

    def clear_new_updates(self):
        self.new_enemy_updates = {}


    def find_closest_target(self, unit):
        best = None
        target = None
        me = unit.location.map_location()
        for enemy in self.enemy_locations:
            them = self.enemy_locations[enemy].location.maplocation()
            distance = me.distance_squared_to(them)
            if best == None or distance < best:
                best = distance
                target = them
        return target


    def find_closest_attackable_target(self, unit):
        best = None
        target = None
        me = unit.location.map_location()
        for enemy in self.enemy_locations:
            them = self.enemy_locations[enemy].location.maplocation()
            distance = me.distance_squared_to(them)
            range = unit.attack_range()
            if distance < range:
                if best == None or distance < best:
                    best = distance
                    target = them
        return target

    def update_closest_target(self, unit, prev):
        me = unit.location.map_location()
        best = me.distance_squared_to(prev)
        target = prev
        ranger_range = 0
        if unit.type == bc.UnitType.Ranger:
            ranger_range = unit.ranger_cannot_attack_range()
        for enemy in self.new_enemy_updates:
            distance = me.distance_squared_to(enemy)
            range = unit.attack_range()
            if ranger_range <= distance < range:
                if best is None or distance < best:
                    best = distance
                    target = enemy
        return target


    @staticmethod
    def get_init_type(ml, planet):
        return {
            "karb": planet.initial_karbonite_at(ml),
            "passable": planet.is_passable_terrain_at(ml),
            # "unit": None,
            # "foe": None
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

    def is_unit_at_location_foe(self, planet, location):
        if isinstance(location, bc.Location):
            location = location.map_location()
        if isinstance(location, bc.MapLocation):
            x = location.x
            y = location.y
            location = (x, y)
        if planet == bc.Planet.Mars:
            return self.mars_map[location]["foe"]
        if planet == bc.Planet.Earth:
            return self.earth_map[location]["foe"]
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
            raise TypeError

    def update_karb_amount(self, location, gc, coords):
        if location.planet == bc.Planet.Earth:
            self.earth_map[coords]["karb"] = gc.karbonite_at(location)
            if gc.karbonite_at(location) == 0:
                self.earth_karboniteLocations.remove(location)
        elif location.planet == bc.Planet.Mars:
            self.mars_map[coords]["karb"] = gc.karbonite_at(location)
            if gc.karbonite_at(location) == 0:
                self.mars_karboniteLocations.remove(location)
            elif location not in self.mars_karboniteLocations:
                self.mars_karboniteLocations.append(location)





