import scipy as sp
import matplotlib.pyplot as plt

from main.api.data.data import PlayerHandler


class Stat:
	"""docstring for Stat"""

	def __init__(self, player_id=0):
		self.player_id = player_id

	def get_player_stats(self):
		player = PlayerHandler().get_player_with_stats(self.player_id)
		player_performance = PlayerHandler().get_player_perf(self.player_id)
		self.player_performance = player_performance
		self._recent = player_performance
		self.create_model()
		current = {'current': self.current}
		expected = {'expected': self.expected}
		player.update(current)
		player.update(expected)
		return player

	def get_expected(self):
		recent = list(self._recent)
		top = recent[-1]
		delimeter = top['week']
		expected = []
		for week in range(delimeter, delimeter + 10):
			exp = {}
			exp['week'] = week
			exp['performance'] = week + 10
			expected.append(exp)
		return expected

	def create_model(self):
		try:
			x = [ perf['week'] for perf in self.player_performance ]
			y = [ perf['performance'] for perf in self.player_performance ]

			exp_x = list(range(x[-1], x[-1] + 5))

			fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
			f1 = sp.poly1d(fp1)
			error1 = self.error(f1, x, y)

			fp2, residuals, rank, sv, rcond = sp.polyfit(x, y, 2, full=True)
			f2 = sp.poly1d(fp2)
			error2 = self.error(f2, x, y)

			fp3, residuals, rank, sv, rcond = sp.polyfit(x, y, 2, full=True)
			f3 = sp.poly1d(fp3)
			error3 = self.error(f3, x, y)

			if error1 < error2 and error1 < error3:
				vect_y = [ int(f1(x_vector)) for x_vector in x ]
				exp_y = [ int(f1(x_vector)) for x_vector in exp_x ]

			elif error2 < error1 and error2 < error3:
				vect_y = [ int(f2(x_vector)) for x_vector in x ]
				exp_y = [ int(f2(x_vector)) for x_vector in exp_x ]

			else:
				vect_y = [ int(f3(x_vector)) for x_vector in x ]
				exp_y = [ int(f3(x_vector)) for x_vector in exp_x ]


			curr_x = x[-40:]
			curr_y = vect_y[-40:]

			self.current = [
					{
						'week': curr_x[i],
						'performance': curr_y[i],
					} for i in range(len(curr_x))
				]
		
			self.expected = [
					{
						'week': exp_x[i],
						'performance': exp_y[i],
					} for i in range(len(exp_x))
				]

		except Exception as e:
			self.current = [
					{
						'week': 0,
						'performance': 0,
					},
					{
						'week': 0,
						'performance': 0,
					}
				]
		
			self.expected = [
					{
						'week': 0,
						'performance': 0,
					},
					{
						'week': 1,
						'performance': 0,
					},
					{
						'week': 2,
						'performance': 0,
					},
					{
						'week': 3,
						'performance': 0,
					},
					{
						'week': 4,
						'performance': 0,
					},
				]
		

	def error(self, f, x, y):
		return sp.sum((f(x) - y) ** 2)

		