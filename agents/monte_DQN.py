import random
import math
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
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
def _monte(board,times = 1000):
    score = 0
    if player_win(board,1):
        print("winning move!",board)
        return times+1
    for _ in range(times):
        cur_player = 2
        b_simu = board.copy()
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
    return score / times
def on_board(x,y):
    return y >= 0 and y < H and x >=0 and x<W
def player_win(board,me):
    for x in range(W):
        for y in range(H):
            if(board[x][y] != me): 
                continue
            for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
                p = 1
                while on_board((x+p*dx)%W,y+p*dy) and board[(x+p*dx)%W][y+p*dy] == me:
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
def gen_obs(board):
    opponent = 2
    player = 1
    empty_positions = np.where(board == 0, 1, 0)
    player_chips   = np.where(board == player, 1, 0)
    opponent_chips = np.where(board == opponent, 1, 0)
    return np.array([empty_positions, player_chips, opponent_chips],dtype=np.uint8)
class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3,5,3) # 5*6*3 => 3 * 4 * 5
        self.conv2 = nn.Conv2d(5,3,3) # 1 * 2 * 3
        self.fc1 = nn.Linear(6,1)
        self.criterion = nn.MSELoss(reduction='mean')
        
    def forward(self, state):
        hid = self.conv1(state)# torch.tanh()
        hid = self.conv2(hid)
        hid = hid.reshape((1,6))
        ret = self.fc1(hid).reshape((1))
        return ret


class MonteDQNAgent():
    def __str__(self):
        return "Monte Agent"
    def __init__(self,num_sample = 1000):
        self.num_sample = num_sample
        self.sample_scheduler = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.network = DQN()
        self.network.to(self.device)
        self.loss_list = []
        self.epoch = 0
        print(f"current device:{self.device}")
    def game_starts(self,obs):
        # shape of obs is (3,width,height)
        global H
        global W
        W = len(obs[0])
        H = len(obs[0][0])
        board = np.zeros((W,H))
        self.network.train()
        self.epoch+=1


    def make_move(self,obs,valid_moves):
        board = obs[1] + obs[2] * 2 # 1是自己 2是對手
        print(board)
        value = -math.inf
        best_move = [random.choice(valid_moves[0]),random.choice(valid_moves[1])]
        # print("valid_moves",valid_moves)
        for col in valid_moves[0]:
            for row in valid_moves[1]:
                board_simu = board.copy()
                move_board(board_simu,col,row,1)

                cur_val = _monte(board_simu,self.num_sample)
                ### Train
                label_val = torch.tensor(cur_val).to(self.device).reshape((1))
                obs = gen_obs(board_simu) 
                obs = torch.tensor(obs,dtype=torch.float).to(self.device) 
                pred_val = self.network(obs)
                mse_loss = self.network.criterion(pred_val,label_val)
                mse_loss.backward()
                self.loss_list.append(mse_loss.detach().cpu().item())
                ###

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
        if self.epoch % 10 == 0:
            torch.save(self.network.state_dict(), f"./model/{self.epoch}.pth")

    def plot_loss(self):
        x_1 = range(len(self.loss_list))

        plt.plot(x_1, loss_list, c='tab:red', label='train')
