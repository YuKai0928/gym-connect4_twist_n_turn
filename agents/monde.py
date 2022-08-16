import random
import math
import numpy as np
board = None
W = 0
H = 0
def get_moves(B):
    """
    :returns: array with all possible moves, index of columns which aren't full and available rotation operation number
    """
    moves = [[col for col in range(W) if B[col][H - 1] == 0],[0]]
    for i in range(W):
        rotatable = False
        for j in range(H):
            if B[i][j] != 0:
                moves[1].append(i+1)
                moves[1].append(H+i+1)
                rotatable = True
                break
        if not rotatable:
            break
    return moves
def _monde(board,col,row,times = 1000):
    score = 0
    b_copy = board.copy()
    move_board(b_copy,col,row,1)
    if player_win(b_copy,1):
        print("winning move!",b_copy)
        return times+1
    for _ in range(times):
        cur_player = 2
        b_simu = b_copy.copy()
        while True:
            valid_moves = get_moves(b_simu)
            if len(valid_moves[0]) == 0:
                break
            col, row = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
            move_board(b_simu,col,row,cur_player)
            if player_win(b_simu,1):
                score+=1
                break
            elif player_win(b_simu,2):
                score-=1
                break
            cur_player = 3 - cur_player
    print(f"MONDE: score = {score}")
    return score / times
def y_on_board(y):
    return y >= 0 and y < H
def player_win(board,me):
    for x in range(W):
        for y in range(H):
            if(board[x][y] != me): 
                continue
            for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
                p = 1
                while y_on_board(y+p*dy) and board[(x+p*dx)%W][y+p*dy] == me:
                    p += 1
                    if p >= 4:
                        # print(f"Finished! winner is {me} at {x} {y} {dx} {dy}, {p=},{board=}")
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

    
class MondeAgent():
    def __str__(self):
        return "Monde Agent"
    def __init__(self,num_sample = 1000):
        self.num_sample = num_sample
        self.sample_scheduler = None
    def game_starts(self,obs):
        # shape of obs is (3,width,height)
        global H
        global W
        W = len(obs[0])
        H = len(obs[0][0])
        board = np.zeros((W,H))
    def make_move(self,obs,valid_moves):
        board = obs[1] + obs[2] * 2 # 1是自己 2是對手
        print(board)
        value = -math.inf
        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
        # print("valid_moves",valid_moves)
        for col in valid_moves[0]:
            for row in valid_moves[1]:
                cur_val = _monde(board,col,row,self.num_sample)
                if cur_val > value:
                    best_move = [col,row]
                    value = cur_val
                if value > self.num_sample:
                    # print("found winning move",best_move)
                    return best_move
        # print(f"return value is {value},move={best_move}")
        return best_move
	
    def opponent_move(self,obs):
        pass
	
    def game_terminates(self,reward):
        pass
