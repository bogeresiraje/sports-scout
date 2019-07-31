from main.app import db
from main.api.data.pi_rate import PiRate
from main.api.data.data import PerformanceHandler, StatsHandler, PlayerHandler

class SetPerformance:
	def __init__(self, player_id=1, player_status='home', home_score=0, away_score=0, home_id=0, away_id=0,
		shots_for=0, shots_for_ontarget=0, goals_for=0, assists=0, crosses=0, crosses_successful=0,
		interceptions=0, clearances=0, tackles=0, fouls=0, shots_against=0, shots_blocked=0, goals_against=0,
		saves=0):

		self.player_id = int(player_id)
		self.player_status = player_status
		self.home_id = int(home_id)
		self.away_id = int(away_id)
		self.home_score = int(home_score)
		self.away_score = int(away_score)
		self.shots_for = int(shots_for)
		self.shots_for_ontarget = int(shots_for_ontarget)
		self.goals_for = int(goals_for)
		self.assists = int(assists)
		self.crosses = int(crosses)
		self.crosses_successful = int(crosses_successful)
		self.interceptions = int(interceptions)
		self.clearances = int(clearances)
		self.tackles = int(tackles)
		self.fouls = int(fouls)
		self.shots_against = int(shots_against)
		self.shots_blocked = int(shots_blocked)
		self.goals_against = int(goals_against)
		self.saves = int(saves)

		player = PlayerHandler().get_player(player_id)
		self.curr_perf = player['curr_perf']
		self.compute_performance()

	def compute_performance(self):
		self.evaluate()
		pirate = PiRate(home_id=self.home_id, away_id=self.away_id, h_score=self.home_score,
			a_score=self.away_score)
		rate_dict = pirate.get_rating()
		if self.player_status == 'home':
			own_club_rating = rate_dict['homeclub_home_rating']
			other_club_rating = rate_dict['awayclub_away_rating']
		else:
			own_club_rating = rate_dict['awayclub_away_rating']
			other_club_rating = rate_dict['homeclub_home_rating']

		coefficient = ((own_club_rating - other_club_rating) * 0.5 + (self.new_perf - self.curr_perf)) * 0.1
		self.performance = self.curr_perf + coefficient

		PlayerHandler().update_player_perf(self.player_id, round(self.performance, 4))
		PerformanceHandler().set_performance(self.player_id, round(self.performance, 4))
		StatsHandler().set_stats(player_id=self.player_id, shots_for=self.shots_for,
			shots_for_ontarget=self.shots_for_ontarget, goals_for=self.goals_for, assists=self.assists,
			crosses=self.crosses, crosses_successful=self.crosses_successful,
			interceptions=self.interceptions, clearances=self.clearances, tackles=self.tackles,
			fouls=self.fouls, shots_against=self.shots_against, shots_blocked=self.shots_blocked,
			goals_against=self.goals_against, saves=self.saves )

	def evaluate(self):
		highest_shots_against = StatsHandler().get_highest_shots_against()
		highest_saves = StatsHandler().get_highest_saves()
		highest_interceptions = StatsHandler().get_highest_interceptions()
		highest_clearances = StatsHandler().get_highest_clearances()
		highest_goals_against = StatsHandler().get_highest_goals_against()
		highest_shots_blocked = StatsHandler().get_highest_shots_blocked()
		highest_tackles = StatsHandler().get_highest_tackles()
		highest_fouls = StatsHandler().get_highest_fouls()
		highest_assists = StatsHandler().get_highest_assists()
		highest_shots_for = StatsHandler().get_highest_shots_for()
		highest_shots_for_ontarget = StatsHandler().get_highest_shots_for_ontarget()
		highest_goals_for = StatsHandler().get_highest_goals_for()
		highest_crosses = StatsHandler().get_highest_crosses()
		highest_crosses_successful = StatsHandler().get_highest_crosses_successful()

		# Shots by opponent
		if highest_shots_against == 0:
			perf_shots_against = 0
		elif highest_shots_against < self.shots_against:
			perf_shots_against = 1
		else:
			perf_shots_against = self.shots_against / highest_shots_against 

		# Saves
		if highest_saves == 0:
			perf_saves = 0
		elif highest_saves < self.saves:
			perf_saves = 1
		else:
			perf_saves = self.saves / highest_saves

		# Interceptions
		if highest_interceptions == 0:
			perf_interceptions = 0
		elif highest_interceptions < self.interceptions:
			perf_interceptions = 1
		else:
			perf_interceptions = self.interceptions / highest_interceptions

		# Clearances
		if highest_clearances == 0:
			perf_clearances = 0
		elif highest_clearances < self.clearances:
			perf_clearances = 1
		else:
			perf_clearances = self.clearances / highest_clearances

		# Shots blocked
		if highest_shots_blocked == 0:
			perf_shots_blocked = 0
		elif highest_shots_blocked < self.shots_blocked:
			perf_shots_blocked = 1
		else:
			perf_shots_blocked = self.shots_blocked / highest_shots_blocked

		if perf_shots_against == 0:
			baye_shots_blocked = 0
		else:
			baye_shots_blocked = (perf_shots_blocked * perf_shots_against) / perf_shots_against

		# Tackles
		if highest_tackles == 0:
			perf_tackles = 0
		elif highest_tackles < self.tackles:
			perf_tackles = 1
		else:
			perf_tackles = self.tackles / highest_tackles

		# Fouls
		if highest_fouls == 0:
			perf_fouls = 0
		elif highest_fouls < self.fouls:
			perf_fouls = 1
		else:
			perf_fouls = self.fouls / highest_fouls

		if perf_tackles == 0:
			baye_fouls = 0
		else:
			baye_fouls = (perf_fouls * perf_tackles) / perf_tackles

		# Goals
		if highest_goals_against == 0:
			perf_goals_against = 0
		elif highest_goals_against < self.goals_against:
			perf_goals_against = 1
		else:
			perf_goals_against = self.goals_against / highest_goals_against

		# Shots to Opponent
		if highest_shots_for == 0:
			perf_shots_for = 0
		elif highest_shots_for < self.shots_for:
			perf_shots_for = 1
		else:
			perf_shots_for = self.shots_for / highest_shots_for

		# Shots on target on opponent
		if highest_shots_for_ontarget == 0:
			perf_shots_for_ontarget = 0
		elif highest_shots_for_ontarget < self.shots_for_ontarget:
			perf_shots_for_ontarget = 1
		else:
			perf_shots_for_ontarget = self.shots_for_ontarget / highest_shots_for_ontarget

		if perf_shots_for == 0:
			baye_shots_for_ontarget = 0
		else:
			baye_shots_for_ontarget = (perf_shots_for_ontarget * perf_shots_for) / perf_shots_for

		# Goals scored against opponent
		if highest_goals_for == 0:
			perf_goals_for = 0
		elif highest_goals_for < self.goals_for:
			perf_goals_for = 1
		else:
			perf_goals_for = self.goals_for / highest_goals_for

		# Crosses
		if highest_crosses == 0:
			perf_crosses = 0
		elif highest_crosses < self.crosses:
			perf_crosses = 1
		else:
			perf_crosses = self.crosses / highest_crosses

		# Crosses successful
		if highest_crosses_successful == 0:
			perf_crosses_successful = 0
		elif highest_crosses_successful < self.crosses_successful:
			perf_crosses_successful = 1
		else:
			perf_crosses_successful = self.crosses_successful / highest_crosses_successful

		if perf_crosses == 0:
			baye_crosses_successful = 0
		else:
			baye_crosses_successful = (perf_crosses_successful * perf_crosses) / perf_crosses

		if highest_assists == 0:
			perf_assists = 0
		elif highest_assists < self.assists:
			perf_assists = 1
		else:
			perf_assists = self.assists / highest_assists

		# Calculate performance
		self.new_perf = (perf_shots_against + perf_assists + perf_saves + perf_interceptions + 
				perf_clearances + baye_shots_blocked + perf_tackles + baye_fouls + perf_goals_against + 
				perf_shots_for +
				baye_shots_for_ontarget + perf_goals_for + perf_crosses + baye_crosses_successful
			) / 4

	def get_performance(self):
		return self.performance
