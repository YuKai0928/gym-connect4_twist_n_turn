import gym
import gym_connect4_twist_n_turn
import random
env = gym.make('Connect4_Twist_n_Turn-v0') # default board size is height=5, width=6
env.reset()
done = False
player = 1
while not done:
    all_action = env.get_moves()
    action = [random.choice(all_action[0]),random.choice(all_action[1])]
    print(f"player {player}'s action {action}")
    observation, reward, done, _ = env.step(action)
    env.render()
    player = 3 - player

print(f"Winner is player {env.winner}")