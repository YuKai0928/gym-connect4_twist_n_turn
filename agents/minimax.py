import random
import math

board = None
W = 0
H = 0
def _monde(obs):
    score = 1
    return score
def y_on_board(y):
    return y >= 0 and y < H
def player_win(self, me):
    for x in range(W):
        for y in range(H):
            if(board[x][y] != me): 
                continue
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            p = 1
            while y_on_board(y+p*dy) and board[(x+p*dx)%W][y+p*dy] == me:
                p += 1
            if p >= self.connect:
            # print(f"Finished! winner is {me} at {x} {y} {dx} {dy}")
                return True
    return False

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


def minimax(board, alpha, beta, maximizing_player,valid_moves):

    if player_win(1):
        return (None, 1)
    elif player_win(2):
        return (None, -1)
    elif len(valid_moves[0]) == 0:
        return (None, 0)

    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf
        ret_value = 0
        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decresed depth and switched player
        for col in valid_moves[0]:
            for row in valid_moves[1]:
                b_copy = board.copy()
                drop_piece(b_copy, col, row, 1)
                # recursive call
                new_score = minimax(b_copy, alpha, beta, False)[1]
                # if the score for this column is better than what we already have
                ret_value += new_score
                if new_score > value:
                    value = new_score
                    best_move = [col,row]
                # alpha is the best option we have overall
                alpha = max(value, alpha) 
                # if alpha (our current move) is greater (better) than beta (opponent's best move), then 
                # the oponent will never take it and we can prune this branch
                if alpha >= beta:
                    break
            if alpha >= beta:
                break
        ret_value /= (len(valid_moves[0]) * len(valid_moves[1]))
        return best_move, ret_value
    else: # for thte minimizing player
        value = math.inf
        ret_value = 0
        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
        for col in valid_moves[0]:
            for row in valid_moves[1]:
                b_copy = board.copy()
                drop_piece(b_copy, col, row, 2)
                new_score = minimax(b_copy, alpha, beta, True)[1]
                ret_value += new_score
                if new_score < value:
                    value = new_score
                    best_move = [col,row]
                beta = min(value, beta) 
                if alpha >= beta:
                    break
            if alpha >= beta:
                break
        return column, ret_value
    
class RandomAgent():
	def __init__(self):
		pass
	def game_starts(self,obs):
        # shape of obs is (3,width,height)
        W = len(obs[0])
        H = len(obs[0][0])
		board = np.zeros((W,H))
	def make_move(self,obs,valid_moves):
        board = obs[1] + obs[2] * 2 # 1是自己 2是對手
        move, ret_val = minimax(board, 5, -math.inf, math.inf, True, valid_moves)
        print(f"return value is {ret_val}")
		return move
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		pass
