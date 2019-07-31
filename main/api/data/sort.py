
'''
	NOTE: insertion sort algorithm.
'''

class Sort:
	def __init__(self, sequence):
		self._sequence = sequence
		self.sort_by_goals_for()
		self.sort_by_goal_diff()
		self.sort_sequence()

	# returns sorted sequence
	def sorted_sequence(self):
		return self._sequence

	# sorts sequence according to points; the highest priority
	def sort_sequence(self):
		seq_copy = self._sequence
		for i in range(1, len(seq_copy)):
			curr_obj = seq_copy[i]
			curr_points = curr_obj.points
			j = i
			while j > 0 and seq_copy[j-1].points > curr_points :
				seq_copy[j] = seq_copy[j-1]
				j -= 1

			seq_copy[j] = curr_obj

		self._sequence = seq_copy

	# sort according to goal difference, second priority
	def sort_by_goal_diff(self):
		seq_copy = self._sequence
		for i in range(1, len(seq_copy)):
			curr_obj = seq_copy[i]
			curr_diff = curr_obj.goal_diff
			j = i
			while j > 0 and seq_copy[j-1].goal_diff > curr_diff:
				seq_copy[j] = seq_copy[j-1]
				j -= 1

			seq_copy[j] = curr_obj

		self._sequence = seq_copy

	# sort by goals scored, third priority
	def sort_by_goals_for(self):
		seq_copy = self._sequence
		for i in range(1, len(seq_copy)):
			curr_obj = seq_copy[i]
			curr_for = curr_obj.goals_for
			j = i
			while j > 0 and seq_copy[j-1].goals_for > curr_for:
				seq_copy[j] = seq_copy[j-1]
				j -= 1

			seq_copy[j] = curr_obj

		self._sequence = seq_copy


class CustomSort(object):
	def __init__(self, sequence=None):
		self._sequence = sequence

	def sort_by_rating(self):
		seq_copy = self._sequence
		for i in range(1, len(seq_copy)):
			curr_obj = seq_copy[i]
			curr_for = curr_obj['curr_perf']
			j = i
			while j > 0 and seq_copy[j-1]['curr_perf'] < curr_for:
				seq_copy[j] = seq_copy[j-1]
				j -= 1

			seq_copy[j] = curr_obj

		return seq_copy
