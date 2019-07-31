from main.api.data.generic import Generic


# Handles players according to one's preferences
class Custom:
	_players = []

	def __init__(self, username):
		self.initialize_players()

	def initialize_players(self):
		generic = Generic()
		self._players = generic.get_generic_players()

	def get_custom_players(self):
		return self._players
