import random

def board_rater(obs):
    """
    Checks whether a newly dropped chip and rotation operation wins the game.
    :param me: player index
    :returns: (boolean) True if the previous move has won the game
    """
    # print('current board:',self.board,"for",me)
    width = len(obs)
    height = len(obs[0])
    def y_on_board(self, y):
    	return y >= 0 and y < height
    score = 0
    for x in range(width):
        for y in range(height):
	        if(obs[x][y] == 0): 
	            continue
	    p = 1
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            while y_on_board(y+p*dy) and obs[(x+p*dx)%self.width][y+p*dy] == 1:
                p += 1
            if p > 1:
            	score += 1
            if p > 2:
                score += 1
            if p > 3:
            	score += 5
    return score
class RandomAgent():
	def __init__(self):
		pass
	def __str__(self):
        return "Random Agent"
	def game_starts(self,obs):
		pass
	def make_move(self,obs,valid_moves):
		return [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass
