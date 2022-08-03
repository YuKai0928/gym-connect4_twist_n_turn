import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Box, MultiDiscrete, Discrete, Tuple
from colorama import Fore
from typing import List
from copy import deepcopy
import numpy as np

class Connect4_TnT_Env(gym.Env):
  metadata = {'render.modes': ['human']}

  """
  get 4 of your colored discs in a row (horizontally/vertically/diagonally)
  board: 0 for empty, 1 for disc of P1, 2 for disc of P2
  y
  ^
  |
  |
  | board[x][y]
  |
 0L-----> x
  0
  action : Tuple(Lay width index, Rotate action num)
  Rotate action num: 0 if don't rotate; layer index [1,height] + height if ClockWise else 0
    e.g. 3 => rotate the 4th layer Counter Clock Wise
  self.winner = None(gaming) / 1 / 2 / -1(draw)
  """
  def __init__(self,width=6, height=5, connect=4):
    self.width = width
    self.height = height
    self.connect = connect
    self.num_players = 2
    self.winner = None
    # 3: Channels. Empty cells, p1 chips, p2 chips
    player_observation_space = Box(low=0, high=1,shape=(3,self.width, self.height),dtype=np.int32)
    self.observation_space = Tuple([player_observation_space for _ in range(self.num_players)])
    self.action_space = Tuple([MultiDiscrete([self.width, 1+self.height*2]) for _ in range(self.num_players)]) # 
    self.state_space_size = (self.height * self.width) ** 3 # w*h cells in total, each can be empty/P1 Disc/P2 Disc
    self.reset()
  def step(self, action):
    lay, rot = action
    if not(lay >=0 and lay < self.width) or not (board[lay][self.height-1] == 0):
      raise IndexError(f"Only lay in the range [0,{self.width-1}] and the column with space")
    y = self.height-1
    while(board[lay][y] == 0 and y>0):
      y-=1

    board[lay][y+1] = self.current_player
    
    # Only check terminate state after all the actions(lay&rotate) are done
    if(rot!=0):
      direction = rot-1 // self.height # 1 for CW, 0 for CCW
      y = rot-1 % self.height
      if(direction):
        tmp=board[0][y]
        for i in range(self.width-1):
          board[i][y] = board[(i+1)%self.width][y]
        board[self.width-1][y] = tmp
      else:
        tmp=board[0][y]
        for i in range(self.width-1,0,-1):
          board[(i+1)%self.width][y] = board[i][y]
        board[1][y] = tmp
      if y>0: # make sure all the discs are falled in the right position
        for i in range(self.width):
          tmp_y = 0 # target y
          while(board[i][tmp]>0):
            tmp_y+=1
          if tmp_y < y:
            for j in range(y,self.height):
              board[i][tmp_y-y+j] = board[i][j]
              board[i][j] = 0
    self.winner, reward_vector = self.check_termination()

    info = {'legal_actions': self.get_moves(),
            'current_player': self.current_player}
    self.current_player = 2 if self.current_player == 1 else 1
    return self.get_player_observations(), reward_vector, \
           self.winner is not None, info

  def reset(self):
    self.board = np.zeros((self.width, self.height))
    self.current_player = 1 # Player 1 will move first.
    self.winner = None # -1/None/1/2
    return self.get_player_observations()
  def render(self, mode='human'):
    s = ""
    for x in range(self.height - 1, -1, -1):
        for y in range(self.width):
            s += {0: Fore.WHITE + '.', 1: Fore.RED + 'X', 2: Fore.YELLOW + 'O'}[self.board[y][x]]
            s += Fore.RESET
        s += "\n"
    print(s)

  def close(self):
    pass

  ### Other Utility Function
  
  def get_result(self, player):
    """
    :param player: (int) player which we want to see if he / she is a winner
    :returns: winner from the perspective of the param player
    """
    if self.winner == -1: return 0  # A draw occurred
    return +1 if player == self.winner else -1


  def check_termination(self):
    winner, reward_vector = self.winner, [0, 0]
    if self.player_win(1):
      reward_vector = [1, -1]
    elif self.player_win(2):
      reward_vector = [-1, 1]
    elif self.get_moves()[0] == []:  # A draw has happened
      winner = -1
      reward_vector = [0, 0]
    return winner, reward_vector

  def player_win(self, me):
    """
    Checks whether a newly dropped chip and rotation operation wins the game.
    :param me: player index
    :returns: (boolean) True if the previous move has won the game
    """
    for x in range(self.width):
      for y in range(self.height):
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
          p = 1
          while self.y_on_board(y+p*dy) and self.board[(x+p*dx)%self.width][y+p*dy] == me:
            p += 1
          # n = 1
          # while self.is_on_board(x-n*dx, y-n*dy) and self.board[x-n*dx][y-n*dy] == me:
          #     n += 1

          # if p + n >= (self.connect + 1): # want (p-1) + (n-1) + 1 >= 4, or more simply p + n >= 5
          
          if p >= self.connect:
              return True
    return False
  def y_on_board(self, y):
    return y >= 0 and y < self.height

  def get_player_observations(self) -> List[np.ndarray]:
    p1_state = self.filter_observation_player_perspective(1)
    p2_state = np.array([np.copy(p1_state[0]),
                         np.copy(p1_state[-1]), np.copy(p1_state[-2])])
    return [p1_state, p2_state]
  def get_moves(self):
    """
    :returns: array with all possible moves, index of columns which aren't full and available rotation operation number
    """
    if self.winner is not None:
        return []
    return Tuple([col for col in range(self.width) if self.board[col][self.height - 1] == 0],[i for i in range()])

  def filter_observation_player_perspective(self, player: int) -> List[np.ndarray]:
    opponent = 1 if player == 2 else 1
    # One hot channel encoding of the board
    empty_positions = np.where(self.board == 0, 1, 0)
    player_chips   = np.where(self.board == player, 1, 0)
    opponent_chips = np.where(self.board == opponent, 1, 0)
    return np.array([empty_positions, player_chips, opponent_chips])
