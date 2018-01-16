import battlecode as bc

def fill_research_queue(gc):
    """
    Establishes the full research queue for the entire game.
    """
    gc.queue_research(bc.UnitType.Knight) #25 turns. Put second because it quickly gives us a combat advantage
    gc.queue_research(bc.UnitType.Mage) #25 turns. Put second because it quickly gives us a combat advantage
    gc.queue_research(bc.UnitType.Rocket) #100 turns. Put third because of the time it takes to get to Mars at 100 turns
    gc.queue_research(bc.UnitType.Worker) #25 turns
    gc.queue_research(bc.UnitType.Mage) #75 turns
    gc.queue_research(bc.UnitType.Mage) #100 turns
    gc.queue_research(bc.UnitType.Mage) #200 turns
    gc.queue_research(bc.UnitType.Healer) #25 turns
    gc.queue_research(bc.UnitType.Rocket) #100 turns. Speeds up travel time which we need if we are not on Mars yet
