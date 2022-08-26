import gym
import gym_connect4_twist_n_turn
import random
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.monde import MondeAgent
from agents.minimax import MinimaxAgent
from agents.monte_DQN import MonteDQNAgent
env = gym.make('Connect4_Twist_n_Turn-v0') # default board size is height=5, width=6
obs = env.reset()
done = False
player = 0
players = [MonteDQNAgent(3000),MinimaxAgent(4)]
for i in players:
    i.game_starts(obs[0])
legal_actions = env.get_moves()
env.render()
while not done:
    # print(f"obs 0 {obs[0]}\n======\nobs 1 {obs[1]}")
    action = players[player].make_move(obs[player],legal_actions)
    obs, reward, done, info = env.step(action)
    legal_actions = info['legal_actions']

    players[1-player].opponent_move(obs[1-player])

    print(f"player {player+1}'s action {action}")
    env.render()
    player = 1 - player # player index 0 or 1 alternates
for i in range(2):
    players[i].game_terminates(reward[i])

print(f"Winner is player {players[env.winner-1]}")
players[0].plot_loss()