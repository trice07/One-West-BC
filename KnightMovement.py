import battlecode as bc
import Navigation


def moveToEnemy(gc, unit):
    """
    Move Knights in direction of nearest enemy
    :param gc: game controller
    :param unit: Unit object
    :return: None
    """
    vision = gc.get_team_array(gc.planet())[0]
    lilBitch = vision.find_closest_target(unit)
    Navigation.Bug(gc, unit, lilBitch)


def lure(gc, unit):
    """
    If we can sense knights in a 2 square radius it is more effective to wait for them to enter our attack radius.
    This should be checked before moving the enemy (if there are no enemies in a one square radius)
    :param gc: game controller
    :param unit: unit object
    :return: Boolean representing if the knight should wait or not
    """
    enemyTeam = bc.Team.red if gc.team() == bc.Team.blue else bc.Team.blue
    closeEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, enemyTeam)
    for i in range(len(closeEnemies)):
        if closeEnemies[i].unit_type != bc.UnitType.Worker or closeEnemies[i].unit_type != bc.UnitType.Knight:
            return False
        if closeEnemies[i].unit_type == bc.UnitType.Knight:
            return True
    return False
