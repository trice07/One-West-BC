from Radar import Radar
import battlecode as bc


class Globals:
    radar = None
    us = None
    them = None

    def __init__(self, gc):
        Globals.radar = Radar(gc.starting_map(bc.Planet.Earth), gc.starting_map(bc.Planet.Mars))
        Globals.us = gc.team()
        if Globals.us == bc.Team.Blue:
            Globals.them == bc.Team.Red
        else:
            Globals.them = bc.Team.Blue
