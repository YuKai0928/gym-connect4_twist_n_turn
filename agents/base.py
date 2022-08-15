class BaseAgent():
	def __str__(self):
        return "Your name"
	def __init__(self):
		pass
	def game_starts(self,obs):
		pass
	def make_move(self,obs,valid_moves):
		pass
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass

