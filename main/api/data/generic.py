from main.api.data.data import PlayerHandler

# Handles players that are general to every user
# Data structure and composition is maintained i.e not cutomized
class Generic:
	generic = ''
	_players = []

	def __init__(self, generic='generic'):
		self.generic = generic
		self.initialize()

	def initialize(self):
		self._players = PlayerHandler().get_all_players_with_clubs()

	def get_generic_players(self):
		return self._players