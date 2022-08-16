import random
import math
import numpy as np
board = None
W = 0
H = 0
def board_rater(obs):
    score = 0
    for x in range(W):
        for y in range(H):
            if(obs[x][y] == 1): 
                p = 1
                for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
                    while on_board((x+p*dx)%W,y+p*dy) and obs[(x+p*dx)%W][y+p*dy] == 1:
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
                    while on_board((x+p*dx)%W,y+p*dy) and obs[(x+p*dx)%W][y+p*dy] == 2:
                        p += 1
                        if p == 2:
                            score -= 1
                        if p == 3:
                            score -= 1
                        if p == 4:
                            score -= 5
                            break
    return score
def on_board(x,y):
    return y >= 0 and y < H and x >=0 and x<W
def player_win(b, me):
    for x in range(W):
        for y in range(H):
            if(b[x][y] != me): 
                continue
            for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
                p = 1
                while on_board((x+p*dx)%W,y+p*dy) and  b[(x+p*dx)%W][y+p*dy] == me:
                    p += 1
                    if p >= 4:
                        return True
    return False
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


def minimax(board, depth, alpha, beta, maximizing_player):
    valid_moves = get_moves(board)
    if(depth == 4):
        print(depth, alpha, beta, maximizing_player)
    if player_win(board,1):
        # print("A")
        return (None,100000)
    elif player_win(board,2):
        # print("B")
        return (None,-100000)

    elif len(valid_moves[0]) == 0:
        # print("C")
        return (None,0)
    elif depth == 0:
        return (None,board_rater(board))

    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf
        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]

        for col in valid_moves[0]:
            for row in valid_moves[1]:
                b_copy = board.copy()
                move_board(b_copy, col, row, 1)
                new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
                # if the score for this column is better than what we already have
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
        # print("1",best_move,depth)
        return best_move, value
    else: # for the minimizing player
        value = math.inf

        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
        for col in valid_moves[0]:
            for row in valid_moves[1]:
                b_copy = board.copy()
                move_board(b_copy, col, row, 2)
                new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_move = [col,row]
                beta = min(value, beta) 
                if alpha >= beta:
                    break
            if alpha >= beta:
                break
        # print("2",best_move,depth)
        return best_move, value
    
class MinimaxAgent():
    def __str__(self):
        return "MinimaxAgent"
    def __init__(self,depth):
        self.depth = depth
    def game_starts(self,obs):
        # shape of obs is (3,width,height)
        global W
        global H
        W = len(obs[0])
        H = len(obs[0][0])
        board = np.zeros((W,H))
    def make_move(self,obs,valid_moves):
        board = obs[1] + obs[2] * 2 # 1是自己 2是對手
        # best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
        move = minimax(board, self.depth, -math.inf, math.inf, True)[0]
        
        # print(f"return move {move}")
        return move
    def opponent_move(self,obs):
        pass
    def game_terminates(self,reward):
        pass
