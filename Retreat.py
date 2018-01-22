

def retreatFromKnownEnemy(gc, unit, enemy):
    """
    Move such that distance from known enemy increases.
    :param gc: game controller
    :param unit: unit object
    :param enemy: unit object of the enemy
    :return: True if able to move, False otherwise
    """
    enemyLocation = enemy.location.map_location()
    unitLocation = unit.location.map_location()
    direction = unitLocation.direction_to(enemyLocation)
    retreatDirection = direction.opposite()
    if gc.can_move(unit, retreatDirection):
        gc.move_robot(unit, retreatDirection)
        return True

    else:
        currentDistance = unitLocation.distance_squared_to(enemyLocation)
        for i in range(8):
            retreatDirection = retreatDirection.rotate_right()
            if unitLocation.add(retreatDirection).distance_squared_to(enemyLocation) > currentDistance:
                if gc.can_move(unit, retreatDirection):
                    gc.move_robot(unit, retreatDirection)
                    return True
        return False




def retreat(gc, unit):
    """
    Run away
    :param gc: game controller
    :param unit: unit object
    :return: None
    """
    currentLocation = unit.location.map_location()
    enemy = bc.Team.red if gc.team() == bc.Team.blue else bc.Team.blue
    enemies = gc.sense_nearby_units_by_team(currentLocation, 50, enemy)
    central = findEnemyCenter(gc, enemies)
    reflection = reflectPoint(central)
    Bug(gc, unit, reflection, True)
