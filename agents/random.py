import random
class RandomAgent():
	def __init__(self):
		pass
	def game_starts(self,obs):
		pass
	def make_move(self,obs,valid_moves):
		return [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass
