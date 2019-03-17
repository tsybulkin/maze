#
# Reinforcement learning
#

import numpy as np

FOOD_NBR = 25
GHOST_INIT_PLACES = [ np.array([0, 0]), np.array([9, 9]), np.array([0, 9]), np.array([9, 0]) ]

class World():
	def __init__(self, ghost_nbr):
		self.ghost_nbr = ghost_nbr
		self.walls = []
		self.ghosts = []
		self.ghost_directs = []
		self.agent = None
		self.food = set()

	
	def initialize(self):
		for i in range(10):
			self.walls.append(np.random.choice([True, False], p=np.array([0.1, 0.9]), size=10))

		indices = np.random.choice(len(GHOST_INIT_PLACES), size=self.ghost_nbr)
		self.ghosts = [ GHOST_INIT_PLACES[ind].copy() for ind in indices]

		for g in self.ghosts:
			directions = self.get_legal_actions(g)
			self.ghost_directs.append(np.random.choice(directions))
		
		self.agent = np.array([5, 5])
		
		for i in range(FOOD_NBR):
			food = tuple(np.random.randint(0, 10, size=2))
			self.food.add(food)

	
	def take_agents_action(self, action):
		assert action in [None, 'up', 'down', 'left', 'right']
		## Agent move
		self.agent += dir2vec(action)
		if self.agent_cought():
			return True, 0

		## Food update
		if tuple(self.agent)  in self.food:
			self.food.remove(tuple(self.agent))
			food = 1
		else:
			food = 0

		## Ghosts moves
		for i in range(len(self.ghosts)):
			g, d = self.ghosts[i], self.ghost_directs[i]
			
			legal_actions = self.get_legal_actions(g)
			legal_actions.remove(None)
			if len(legal_actions) > 1 and (d in legal_actions):
				opp = opposite_move(d)
				if opp in legal_actions:
					legal_actions.remove(opp)

			if np.random.random() < 0.5:
				new_dir = get_agent_directions(g, self.agent, legal_actions)
			elif d in legal_actions and np.random.random() < 0.7:
				new_dir = d
			else:
				new_dir = np.random.choice(legal_actions)
			self.ghosts[i] += dir2vec(new_dir) 
			self.ghost_directs[i] = new_dir

		if self.agent_cought():
			return True, food
		return False, food


	def get_legal_actions(self, coords):
		x, y = coords
		legal_actions = [None]
		if y > 0: legal_actions.append('up')
		if y < 9: legal_actions.append('down')
		if x < 9 and not self.walls[x][y]: legal_actions.append('right')
		if x > 0 and not self.walls[x-1][y]: legal_actions.append('left')

		return legal_actions



	def show(self):
		transposed = np.array(self.walls).T
		maze = []
		for row in transposed:
			maze.append(show_row(row))

		for x,y in self.food:
			row = maze[y]
			maze[y] = row[:1+2*x] + "." + row[2+2*x:]

		for x,y in self.ghosts:
			row = maze[y]
			maze[y] = row[:1+2*x] + "G" + row[2+2*x:]

		x,y = self.agent
		row = maze[y]	
		maze[y] = row[:1+2*x] + "A" + row[2+2*x:]
		print "", "_"*21
		for row in maze:
			print row
		print "", "-"*21

	
	def agent_cought(self):
		return any(np.array_equal(self.agent, g) for g in self.ghosts)




def show_row(row):
	s = "| "
	for r in row:
		if r: s += "| "
		else: s += "  "
	s += "|"
	return s


def dir2vec(d):
	if not d: return np.array([0, 0])
	if d == 'up': return np.array([0, -1])
	if d == 'down': return np.array([0, 1])
	if d == 'left': return np.array([-1, 0])
	if d == 'right': return np.array([1, 0])
	else:
		print "direction:", d 
		raise

def opposite_move(d):
	if d == 'up': return 'down'
	if d == 'down': return 'up'
	if d == 'left': return 'right'
	if d == 'right': return 'left'
	return None


def get_agent_directions(g, a, available_moves):
	v = a - g
	best_moves = []
	if v[0] > 0 and 'right' in available_moves: best_moves.append('right')
	elif v[0] < 0 and 'left' in available_moves: best_moves.append('left')

	if v[1] < 0 and 'up' in available_moves: best_moves.append('up')
	elif v[1] > 0 and 'down' in available_moves: best_moves.append('down')

	if best_moves:
		return np.random.choice(best_moves)
	return np.random.choice(available_moves)


