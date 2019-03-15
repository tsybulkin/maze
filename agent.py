

import numpy as np
from world import get_agent_directions
import os.path
import pickle

ALPHA = 0.25
GAMMA = 0.95


class RandomAgent():
	def __init__(self):
		self.food = 0


	def get_action(self, available_actions,  my_coords=None, food=[], ghosts=[]):
		return np.random.choice(available_actions)
		

	def observe(self, caught, eaten_food, world):
		self.food += eaten_food



class GreedyAgent():
	def __init__(self):
		self.food = 0


	def get_action(self, available_actions, my_coords=None, food=[], ghosts=[]):
		if type(my_coords) is np.ndarray:
			xo,yo = my_coords
		else:
			return np.random.choice(available_actions)

		closest_food, xc, yc = min( (abs(xo-x) + abs(yo-y),x,y) for x,y in food)
		return get_agent_directions(my_coords, (xc,yc), available_actions)


	def observe(self, caught, eaten_food, world):
		self.food += eaten_food




class LearningAgent():
	def __init__(self):
		self.food = 0
		if os.path.isfile('qtab.dat'):
			f = open('qtab.dat','rb')
			self.qTab = pickle.load(f)
			f.close()
		else:
			self.qTab = {}
		self.last_action = None
		self.last_state = None


	def get_action(self, available_actions, my_coords=None, food=[], ghosts=[]):
		if np.random.random() < 0.0:
			self.last_action = np.random.choice(available_actions)
			return self.last_action

		self.last_action = self.get_best_action(available_actions)
		return self.last_action



	def observe(self, caught, eaten_food, world):
		self.food += eaten_food
		
		f1 = get_closest_ghost_direction(world.agent, world.ghosts)
		f2 = get_closest_ghost_distance(world.agent, world.ghosts)
		
		reward = (self.get_reward(caught, eaten_food, (f1,f2)) + 
			(9 - np.linalg.norm(world.agent-np.array([5,5])))/10.)
		state = (f1,f2)
		old_values = self.qTab.get(self.last_state, {})
		old_val = old_values.get(self.last_action, 0)

		new_val = (1-ALPHA) * old_val + ALPHA * (reward + GAMMA * self.get_state_value(state))
		old_values[self.last_action] = new_val
		self.qTab[self.last_state] = old_values

		self.last_state = state


	def get_state_value(self, state):
		values = self.qTab.get(self.last_state, {})
		return max( [0] + [values[a] for a in values.keys()])

	
	def get_best_action(self, available_actions):
		values = self.qTab.get(self.last_state, {})
		best_actions = [ (values[a],a) for a in values.keys() if a in available_actions]
		if len(best_actions) == 0:
			return np.random.choice(available_actions)
		else:
			_, a = max(best_actions)
			return a


	def get_reward(self, caught, eaten_food, state):
		if caught:
			return -50
		return 0.1 * eaten_food



def get_closest_ghost_direction(agent, ghosts):
	xo,yo = agent
	_,x,y = min( (abs(xo-x) + abs(yo-y),x,y) for x,y in ghosts)
	return int(np.arctan2(x-xo, y-yo) + np.pi)



def get_closest_ghost_distance(agent, ghosts):	
	xo,yo = agent
	return min( abs(xo-x) + abs(yo-y) for x,y in ghosts)






		