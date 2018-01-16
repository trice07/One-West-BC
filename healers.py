import battelcode as bc

class Healers(unit): 

	def __init__(self): 

		self.healer_id = unit.id #healer's id number
		self.current_loc = unit.location #the current_location of a healer 

	def random_movement_generator(self): 
		'''
		This method generates a random location for the mage to potentially move to. 
		Inputs: None
		Outputs: returns a random location on the map
		'''
		return random.choice(directions)

	def heal_nearby_squares(self): 
		'''
		This helper method scans the nearby squares to see whether there are enemy bots in the neighboring squares. It also checks that the mage can attack.
		Inputs: None
		Outputs: returns a unit (which includes a location) if there is a neighboring ally bot, NoneType otherwise
		'''
		if self.current_loc.is_on_map(): 
			nearby = GameController.sense_nearby_units(self.current_loc, 2)
			allies = [] #empty list that represents the units in the neighboring squares that can be healed/helped
			for other in nearby: 
				if other.team != my_team and GameController.is_heal_ready(self.healer.id) and GameController.can_heal(self.healer.id, other.id): 
					allies.append(other)
			return self.most_needy_units(allies) #returns the units in the nearby squares that need the most immediate attention
		return None

	def most_needy_units(self, units): 
		'''
		This helper method takes in a list of units and determines which unit is the least healthy. 
		Inputs: units - a list containing the units of interest
		Outputs: returns the unit that is in the most distress, if all have maximum health, then the method returns None
		'''
		minimum = None 
		for unit in units: 
			if minimum is None: 
				if abs(unit.max_health - unit.health) != 0:
					minimum = unit
			elif abs(unit.max_health - unit.health) > abs(minimum.max_health - minimum.health): 
				minimum = unit 
		return minimum 

	def find_others_in_need(self): 
		'''
		This helper method scans the board to see whether there are other bots on the map who need healing. 
		Inputs: None
		Outputs: returns a unit (which includes a location) if there is an ally unit in distress, a NoneType otherwise
		'''


	def manage(self): 
		'''
		This method manages the movements of the healers. 
		Inputs: None
		Outputs: moves the healer and potentially heals 
		'''
		if GameController.is_move_ready(self.healer_id): #check that movement heat is under control

			#check the neighboring squares for any ally units that are in dire need of healing/help 
			most_needy = self.heal_nearby_squares()
			if most_needy is not None: 
				return self.heal(self.healer_id, most_needy.id)

			#scan the rest of the map to see if there are others that need to be helped
			elif False:

			#worst comes to worst, move in a random direction 
			else: 
				direc = self.random_movement_generator() 
				return GameController.move_robot(self.healer_id, direc)



