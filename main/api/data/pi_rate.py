import math
from main.api.data.data import ClubHandler, RatingHandler


class PiRate:
	def __init__(self, home_id=0, away_id=0, h_score=0, a_score=0):
		self.home_id, self.away_id = home_id, away_id
		self.h_score, self.a_score = h_score, a_score

		home_club = ClubHandler().get_club(home_id)
		self.h_home_rating = home_club.home_rating
		self.h_away_rating = home_club.away_rating

		away_club = ClubHandler().get_club(away_id)
		self.a_away_rating = away_club.away_rating
		self.a_home_rating = away_club.home_rating

		self.h_h_rating, self.h_a_rating = 0, 0
		self.a_h_rating, self.a_a_rating = 0, 0

		self.compute_rating()
		self.update_rating()

	def compute_rating(self):
		actual_goal_diff = self.h_score - self.a_score

		home_power = abs(self.h_home_rating) / 3
		away_power = abs(self.a_away_rating) / 3
		exp_home_goal_diff = -(10 ** home_power - 1) if(self.h_home_rating < 0) else(10 ** home_power - 1)
		exp_away_goal_diff = -(10 ** away_power - 1) if(self.a_away_rating < 0) else(10 ** away_power - 1)

		exp_goal_diff = exp_home_goal_diff - exp_away_goal_diff
		error = abs(actual_goal_diff - exp_goal_diff)

		weight_error = 3 * math.log10(1 + error)

		# For Home Club
		if exp_goal_diff < actual_goal_diff:
			self.h_h_rating = self.h_home_rating + weight_error * 0.1
		else:
			self.h_h_rating = self.h_home_rating - weight_error * 0.1

		self.h_a_rating = self.h_away_rating + (self.h_h_rating - self.h_home_rating) * 0.3

		# For away club
		if exp_goal_diff > actual_goal_diff:
			self.a_a_rating = self.a_away_rating + weight_error * 0.1
		else:
			self.a_a_rating = self.a_away_rating - weight_error * 0.1

		self.a_h_rating = self.a_home_rating + (self.a_a_rating - self.a_away_rating) * 0.3

	def update_rating(self):
		RatingHandler().update_club_rating(club_id=self.home_id, home_rating=round(self.h_h_rating, 4),
				away_rating=round(self.h_a_rating, 4)
			)
		RatingHandler().update_club_rating(club_id=self.away_id, home_rating=round(self.a_h_rating, 4),
				away_rating=round(self.a_a_rating, 4)
			)

	def get_rating(self):
		return {
					'homeclub_home_rating': round(self.h_h_rating, 4),
					'homeclub_away_rating': round(self.h_a_rating, 4),
					'awayclub_home_rating': round(self.a_h_rating, 4),
					'awayclub_away_rating': round(self.a_a_rating, 4),
				}
