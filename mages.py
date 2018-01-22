import battlecode as bc

class Mages(unit): 

	def __init__(self):

		self.mage_id = unit.id #mage id number 
		self.current_loc = unit.location #the current_location of a mage

	def random_movement_generator(self): 
		'''
		This method generates a random location for the mage to potentially move to. 
		Inputs: None
		Outputs: returns a random location on the map
		'''
		return random.choice(directions)

	def attack_nearby_squares(self): 
		'''
		This helper method scans the nearby squares to see whether there are enemy bots in the neighboring squares. It also checks that the mage can attack.
		Inputs: None
		Outputs: returns a location if there is a neighboring enemy bot, NoneType otherwise
		'''
		if self.current_loc.is_on_map(): 
			nearby = GameController.sense_nearby_units(self.current_loc.map_location, 2)
			for other in nearby: 
				if other.team != my_team and GameController.is_attack_ready(self.mage_id) and GameController.can_attack(self.mage_id, other.id): 
					return other
		return None

	def blink_location(self): 
		'''
		This helper method finds if there is a place on the map where the team's bots are in trouble. 
		Inputs: None
		Outputs: returns a location to teleport too --> None if there are no places where team's bots are in trouble or a direction if the mage doesn't have to blink
		'''


	def manage(self): 
		'''
		This method controls what the mage homies do. 
		Inputs: None
		Outputs: moves the bot, attacks an enemy, blinks, etc. 
		'''
		if GameController.is_move_ready(self.mage_id): #check that the movement heat is under control
			#MUST MAKE HIERARCHIES FOR WHAT THE MAGES PRIORITIES ARE...

			#scan board and determine whether any hommies need help
			if GameController.is_blink_ready(self.mage_id): #check whether the mage can actually use blink and teleport
				blink_location = self.blink_location() #returns a location, if it is feasible to teleport to another location

				if GameController.can_blink(self.mage_id, blink_location): #if the mage has blink, it's ready, then use it to teleport
					GameController.blink(self.mage_id, blink_location)

			#scan nearby squares and see if there is an enemy bot to attack
			other = self.attack_nearby_squares()
			if other is not None: 
				return GameController.attack(self.mage_id, other.id) #terminate function

			#generate a random direction and send the mage in that direction
			direc = self.random_movement_generator()
			return GameController.move_robot(self.mage_id, direc)





		