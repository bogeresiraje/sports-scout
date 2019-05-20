from main.api.data.data import PlayerHandler


# Returns top scorers ( five )
def top_scorers():
	players = PlayerHandler().get_players_list_by_goals()
	return players[:5]


# Returns five players witht top assists
def top_assists():
	players = PlayerHandler().get_players_list_by_assists()
	return players[:5]


# Returns five players witht top yellow cards
def top_yellow():
	players = PlayerHandler().get_players_list_by_yellow()
	return players[:5]	


# Returns five players witht top red cards
def top_red():
	players = PlayerHandler().get_players_list_by_red()
	return players[:5]
