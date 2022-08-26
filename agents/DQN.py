import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
from torch.optim.lr_scheduler import StepLR
import random

seed = 543 # Do not change this
def fix(env, seed):
	  env.seed(seed)
	  env.action_space.seed(seed)
	  torch.manual_seed(seed)
	  torch.cuda.manual_seed(seed)
	  torch.cuda.manual_seed_all(seed)
	  np.random.seed(seed)
	  random.seed(seed)
	  torch.set_deterministic(True)
	  torch.backends.cudnn.benchmark = False
	  torch.backends.cudnn.deterministic = True
class PolicyGradientNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3,5,3) # 5*6*3 => 3 * 4 * 5
        self.conv2 = nn.Conv2d(5,3,3) # 1 * 2 * 3
        self.fc1 = nn.Linear(6,2)
        self.criterion = nn.MSELoss(reduction='mean')
        
    def forward(self, state):
        hid = torch.tanh(self.conv1(state))
        hid = torch.tanh(hid)
        ret = hid.reshape((6))
        return self.fc1(hid)
class PolicyGradientAgent():
    def __init__(self, network):
        self.network = network
        self.optimizer = optim.SGD(self.network.parameters(), lr=0.001)
        
    def forward(self, state):
        return self.network(state)
    def learn(self, log_probs, rewards):
        loss = (-log_probs * rewards).sum() # You don't need to revise this to pass simple baseline (but you can)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
    def sample(self, state):
        action_prob = self.network(torch.FloatTensor(state))
        action_dist = Categorical(action_prob)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)
        return action.item(), log_prob
class DQNAgent():
	def __str__(self):
        return "DQNAgent"
	def __init__(self):
		network = PolicyGradientNetwork()
		self.agent = PolicyGradientAgent(network)
		self.agent.network.train()  # Switch network into training mode 
		EPISODE_PER_BATCH = 5  # update the  agent every 5 episode
		NUM_BATCH = 500        # totally update the agent for 400 time

		self.avg_total_rewards = []
		self.avg_final_rewards = []
		self.log_probs = []
		self.rewards = []
    	self.total_rewards = [] 
    	self.final_rewards = []
	def game_starts(self,obs):
		self.total_reward = 0
		self.total_step = 0
        self.seq_rewards = []

	def make_move(self,obs,valid_moves):
		action, log_prob = self.agent.sample(obs)
		self.log_probs.append(log_prob)
		self.total_step+=1
		return action
	def opponent_move(self,obs):
		pass
	def game_terminates(self,reward):
		self.final_rewards.append(reward)
        self.total_rewards.append(total_reward)
        rewards = (rewards - np.mean(rewards)) / (np.std(rewards) + 1e-9)  # normalize the reward 
	    agent.learn(torch.stack(log_probs), torch.from_numpy(rewards))
	    print("logs prob looks like ", torch.stack(log_probs).size())
	    print("torch.from_numpy(rewards) looks like ", torch.from_numpy(rewards).size())

