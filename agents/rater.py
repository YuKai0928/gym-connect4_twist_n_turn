import random
import math
import numpy as np
board = None
W = 0
H = 0

def move_board(board,col,row,me):
    for i in range(H):
        if board[col][i] == 0:
            board[col][i] = me 
            break
    if row == 0:
        return
    direction = row // H # 1 for CW, 0 for CCW
    y = (row - 1) % H
    if(direction):
        tmp = board[0][y]
        for i in range(W-1):
            board[i][y] = board[(i+1)%W][y]
        board[W-1][y] = tmp
    else:
        tmp = board[0][y]
        for i in range(W-1,0,-1):
            board[(i+1)%W][y] = board[i][y]
        board[1][y] = tmp
      # make sure all the discs are falled in the right position
    for i in range(W):
        empty_y = 0
        while(empty_y<H and board[i][empty_y]>0):
            empty_y+=1

        move_y = y
        if(board[i][move_y]==0):
            move_y+=1
        if empty_y < move_y:
            for j in range(move_y,H):
                board[i][empty_y-move_y+j] = board[i][j]
                board[i][j] = 0

def board_rater(obs):
    """
    Checks whether a newly dropped chip and rotation operation wins the game.
    :param me: player index
    :returns: (boolean) True if the previous move has won the game
    """
    # print('current board:',self.board,"for",me)
    
    def y_on_board(self, y):
    	return y >= 0 and y < H
    score = 0
    for x in range(W):
        for y in range(H):
	        if(obs[x][y] == 1): 
			    p = 1
		        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
		            while y_on_board(y+p*dy) and obs[(x+p*dx)%W][y+p*dy] == 1:
		                p += 1
			            if p == 2:
			            	score += 1
			            if p == 3:
			                score += 1
			            if p == 4:
			            	score += 5
			            	break
		    elif(obs[x][y] == 2): 
			    p = 1
		        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
		            while y_on_board(y+p*dy) and obs[(x+p*dx)%W][y+p*dy] == 2:
		                p += 1
		            	if p == 2:
			            	score -= 1
			            if p == 3:
			                score -= 1
			            if p == 4:
			            	score -= 5
			            	break
    return score
class RaterAgent():
	def __init__(self):
		pass
	def __str__(self):
        return "Rater Agent"
	def game_starts(self,obs):
		global H
        global W
        W = len(obs[0])
        H = len(obs[0][0])
        board = np.zeros((W,H))
	def make_move(self,obs,valid_moves):
		return [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass
