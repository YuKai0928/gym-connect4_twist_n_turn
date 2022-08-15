class HumanAgent():
	def __init__(self):
		pass
	def game_starts(self,obs):
		pass
	def make_move(self,obs,valid_moves):
		print(obs)
		moves = list(map(int,input().split()))
		return moves
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass